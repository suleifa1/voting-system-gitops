'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { surveyApi } from '@/services/api';
import { Survey, AnswerSubmit } from '@/services/types';
import { authService } from '@/services/auth';
import styles from './survey.module.css';

export default function SurveyPage() {
  const router = useRouter();
  const params = useParams();
  const surveyId = params.id as string;

  const [survey, setSurvey] = useState<Survey | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [answers, setAnswers] = useState<Map<string, string[]>>(new Map());

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/');
      return;
    }
    loadSurvey();
  }, [surveyId]);

  const loadSurvey = async () => {
    try {
      setLoading(true);
      setError(null);

      // Просто загружаем полную анкету с вопросами (БЕЗ startSurvey)
      const data = await surveyApi.getSurvey(surveyId);
      setSurvey(data);

      // Проверяем статус анкеты
      if (data.status !== 'active') {
        setError(`Анкета недоступна для голосования (статус: ${data.status})`);
        setTimeout(() => {
          router.push(`/survey/${surveyId}/results`);
        }, 2000);
        return;
      }

      // Инициализируем пустые ответы
      const initialAnswers = new Map<string, string[]>();
      data.questions?.forEach((question) => {
        initialAnswers.set(question.id, []);
      });
      setAnswers(initialAnswers);
    } catch (err: any) {
      console.error('Error loading survey:', err);
      const errorMessage = err.response?.data?.detail || 'Не удалось загрузить анкету';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleOptionChange = (questionId: string, optionId: string, allowMultiple: boolean) => {
    setAnswers((prev) => {
      const newAnswers = new Map(prev);
      const currentAnswers = newAnswers.get(questionId) || [];

      if (allowMultiple) {
        // Множественный выбор - toggle checkbox
        if (currentAnswers.includes(optionId)) {
          newAnswers.set(
            questionId,
            currentAnswers.filter((id) => id !== optionId)
          );
        } else {
          newAnswers.set(questionId, [...currentAnswers, optionId]);
        }
      } else {
        // Одиночный выбор - radio button
        newAnswers.set(questionId, [optionId]);
      }

      return newAnswers;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Валидация - проверяем что на все вопросы ответили
    const unanswered = survey?.questions?.filter(
      (q) => !answers.get(q.id) || answers.get(q.id)!.length === 0
    );

    if (unanswered && unanswered.length > 0) {
      alert(`Пожалуйста, ответьте на все вопросы. Осталось: ${unanswered.length}`);
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      // Сначала вызываем startSurvey
      try {
        await surveyApi.startSurvey(surveyId);
      } catch (startErr: any) {
        // Если пользователь уже прошел анкету - показываем результаты
        if (startErr.response?.data?.detail?.includes('already completed')) {
          alert('Вы уже прошли эту анкету. Показываем результаты.');
          router.push(`/survey/${surveyId}/results`);
          return;
        }
        throw startErr;
      }

      // Формируем ответы для отправки
      const answersArray: AnswerSubmit[] = Array.from(answers.entries()).map(
        ([question_id, option_ids]) => ({
          question_id,
          option_ids,
        })
      );

      await surveyApi.submitAnswers(surveyId, {
        survey_id: surveyId,
        answers: answersArray,
      });

      // Переход к результатам
      router.push(`/survey/${surveyId}/results`);
    } catch (err: any) {
      console.error('Error submitting answers:', err);
      setError(err.response?.data?.detail || 'Не удалось отправить ответы');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Загрузка анкеты...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>
          <h2>❌ Ошибка</h2>
          <p>{error}</p>
          {error.includes('already completed') && (
            <p className={styles.redirectMessage}>Переход к результатам...</p>
          )}
          <button onClick={() => router.push('/dashboard')} className={styles.backButton}>
            Вернуться к списку
          </button>
        </div>
      </div>
    );
  }

  if (!survey) {
    return null;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <button onClick={() => router.push('/dashboard')} className={styles.backLink}>
          ← Назад к списку
        </button>
        <h1 className={styles.title}>{survey.title}</h1>
        {survey.description && <p className={styles.description}>{survey.description}</p>}
        <div className={styles.info}>
          <span>📋 Вопросов: {survey.questions?.length || 0}</span>
          <span>👥 Прошли: {survey.responses_count}</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className={styles.form}>
        {survey.questions?.map((question, index) => (
          <div key={question.id} className={styles.questionBlock}>
            <div className={styles.questionHeader}>
              <span className={styles.questionNumber}>Вопрос {index + 1}</span>
              {question.allow_multiple_answers && (
                <span className={styles.multipleLabel}>Можно выбрать несколько</span>
              )}
            </div>
            <h3 className={styles.questionText}>{question.question_text}</h3>

            <div className={styles.options}>
              {question.options.map((option) => {
                const isChecked = answers.get(question.id)?.includes(option.id) || false;

                return (
                  <label key={option.id} className={styles.optionLabel}>
                    <input
                      type={question.allow_multiple_answers ? 'checkbox' : 'radio'}
                      name={question.id}
                      value={option.id}
                      checked={isChecked}
                      onChange={() =>
                        handleOptionChange(question.id, option.id, question.allow_multiple_answers)
                      }
                      className={styles.optionInput}
                    />
                    <span className={styles.optionText}>{option.option_text}</span>
                  </label>
                );
              })}
            </div>
          </div>
        ))}

        <div className={styles.submitSection}>
          <button type="submit" disabled={submitting} className={styles.submitButton}>
            {submitting ? 'Отправка...' : 'Отправить ответы'}
          </button>
        </div>
      </form>
    </div>
  );
}
