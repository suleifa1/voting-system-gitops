'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import PollCard from './PollCard';
import styles from './PollsList.module.css';
import { surveyApi } from '@/services/api';
import { SurveyListItem } from '@/services/types';

type FilterType = 'all' | 'active' | 'completed' | 'draft';

export default function PollsList() {
  const [filter, setFilter] = useState<FilterType>('all');
  const [surveys, setSurveys] = useState<SurveyListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    loadSurveys();
  }, []); // Загружаем только один раз при монтировании

  const loadSurveys = async () => {
    try {
      setLoading(true);
      setError(null);
      // Загружаем ВСЕ анкеты без фильтра
      const data = await surveyApi.getSurveys();
      setSurveys(data);
    } catch (err: any) {
      console.error('Error loading surveys:', err);
      setError(err.response?.data?.detail || 'Не удалось загрузить анкеты');
    } finally {
      setLoading(false);
    }
  };

  const handleVote = (surveyId: string) => {
    router.push(`/survey/${surveyId}`);
  };

  const handleView = (surveyId: string) => {
    router.push(`/survey/${surveyId}/results`);
  };

  // Фильтруем анкеты на клиенте
  const filteredSurveys = filter === 'all' 
    ? surveys 
    : surveys.filter(s => s.status === filter);

  // Преобразуем отфильтрованные данные backend в формат компонента PollCard
  const transformedPolls = filteredSurveys.map(survey => ({
    id: survey.id,
    title: survey.title,
    description: survey.description || '',
    status: survey.status,
    endDate: new Date(survey.end_date).toLocaleDateString('ru-RU'),
    votesCount: survey.responses_count,
  }));

  const getCounts = () => {
    const all = surveys.length;
    const active = surveys.filter(s => s.status === 'active').length;
    const completed = surveys.filter(s => s.status === 'completed').length;
    const draft = surveys.filter(s => s.status === 'draft').length;
    return { all, active, completed, draft };
  };

  const counts = getCounts();

  const getFilterButtonClass = (filterType: FilterType) => {
    if (filter === filterType) {
      return `${styles.filterButton} ${styles.filterButtonActive}`;
    }
    return styles.filterButton;
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Loading surveys...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>
          <p>❌ {error}</p>
          <button onClick={loadSurveys} className={styles.retryButton}>
            Try again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {/* Filters */}
      <div className={styles.filters}>
        <div className={styles.filterButtons}>
          <button
            onClick={() => setFilter('all')}
            className={getFilterButtonClass('all')}
          >
            All ({counts.all})
          </button>
          <button
            onClick={() => setFilter('active')}
            className={getFilterButtonClass('active')}
          >
            Active ({counts.active})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={getFilterButtonClass('completed')}
          >
            Completed ({counts.completed})
          </button>
          <button
            onClick={() => setFilter('draft')}
            className={getFilterButtonClass('draft')}
          >
            Drafts ({counts.draft})
          </button>
        </div>
      </div>

      {/* Surveys list */}
      {transformedPolls.length === 0 ? (
        <div className={styles.emptyState}>
          <svg
            className={styles.emptyIcon}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <h3 className={styles.emptyTitle}>No surveys</h3>
          <p className={styles.emptyDescription}>
            There are no surveys in this category yet.
          </p>
        </div>
      ) : (
        <div className={styles.pollsGrid}>
          {transformedPolls.map(poll => (
            <PollCard
              key={poll.id}
              poll={poll}
              onVote={handleVote}
              onView={handleView}
            />
          ))}
        </div>
      )}
    </div>
  );
}
