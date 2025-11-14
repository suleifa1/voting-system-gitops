'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { surveyApi } from '@/services/api';
import { SurveyResults } from '@/services/types';
import styles from './results.module.css';

export default function SurveyResultsPage() {
  const router = useRouter();
  const params = useParams();
  const surveyId = params.id as string;

  const [results, setResults] = useState<SurveyResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResults();
  }, [surveyId]);

  const loadResults = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await surveyApi.getSurveyResults(surveyId);
      setResults(data);
    } catch (err: any) {
      console.error('Error loading results:', err);
      setError(err.response?.data?.detail || 'Не удалось загрузить результаты');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Loading results...</p>
        </div>
      </div>
    );
  }

  if (error || !results) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>
          <h2>❌ Error</h2>
          <p>{error || 'Results not found'}</p>
          <button onClick={() => router.push('/dashboard')} className={styles.backButton}>
            Back to list
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <button onClick={() => router.push('/dashboard')} className={styles.backLink}>
          ← Back to list
        </button>
        <h1 className={styles.title}>{results.survey_title}</h1>
        <div className={styles.info}>
          <div className={styles.infoCard}>
            <span className={styles.infoIcon}>👥</span>
            <div>
              <div className={styles.infoValue}>{results.total_responses}</div>
              <div className={styles.infoLabel}>Total responses</div>
            </div>
          </div>
          <div className={styles.infoCard}>
            <span className={styles.infoIcon}>📋</span>
            <div>
              <div className={styles.infoValue}>{results.questions.length}</div>
              <div className={styles.infoLabel}>Questions</div>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.results}>
        {results.questions.map((question, index) => (
          <div key={question.question_id} className={styles.questionBlock}>
            <div className={styles.questionHeader}>
              <span className={styles.questionNumber}>Question {index + 1}</span>
              <span className={styles.answersCount}>
                {question.total_answers} {question.total_answers === 1 ? 'answer' : 'answers'}
              </span>
            </div>
            <h3 className={styles.questionText}>{question.question_text}</h3>

            <div className={styles.options}>
              {question.options.map((option) => {
                const percentage = option.percentage;
                const isLeading = percentage === Math.max(...question.options.map(o => o.percentage));

                return (
                  <div key={option.option_id} className={styles.optionResult}>
                    <div className={styles.optionHeader}>
                      <span className={styles.optionText}>{option.option_text}</span>
                      <div className={styles.optionStats}>
                        <span className={styles.votesCount}>{option.votes_count} votes</span>
                        <span className={`${styles.percentage} ${isLeading ? styles.leading : ''}`}>
                          {percentage.toFixed(1)}%
                        </span>
                      </div>
                    </div>
                    <div className={styles.progressBar}>
                      <div
                        className={`${styles.progressFill} ${isLeading ? styles.leadingBar : ''}`}
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <div className={styles.actions}>
        <button onClick={() => router.push('/dashboard')} className={styles.backButton}>
          Back to surveys list
        </button>
      </div>
    </div>
  );
}
