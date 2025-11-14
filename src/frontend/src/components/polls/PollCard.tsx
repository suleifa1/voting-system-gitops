'use client';

import styles from './PollCard.module.css';

interface Poll {
  id: string;
  title: string;
  description: string;
  status: 'active' | 'completed' | 'draft';
  endDate?: string;
  votesCount?: number;
}

interface PollCardProps {
  poll: Poll;
  onVote?: (pollId: string) => void;
  onView?: (pollId: string) => void;
}

export default function PollCard({ poll, onVote, onView }: PollCardProps) {
  const getStatusClass = () => {
    switch (poll.status) {
      case 'active':
        return styles.statusActive;
      case 'completed':
        return styles.statusCompleted;
      case 'draft':
        return styles.statusDraft;
      default:
        return styles.statusCompleted;
    }
  };

  const getStatusText = () => {
    switch (poll.status) {
      case 'active':
        return 'Active';
      case 'completed':
        return 'Completed';
      case 'draft':
        return 'Draft';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.cardContent}>
        <div className={styles.header}>
          <h3 className={styles.title}>
            {poll.title}
          </h3>
          <span className={`${styles.statusBadge} ${getStatusClass()}`}>
            {getStatusText()}
          </span>
        </div>
        
        <p className={styles.description}>
          {poll.description}
        </p>

        <div className={styles.metadata}>
          {poll.endDate && (
            <div className={styles.metadataItem}>
              <svg className={styles.icon} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>Until {poll.endDate}</span>
            </div>
          )}
          {poll.votesCount !== undefined && (
            <div className={styles.metadataItem}>
              <svg className={styles.icon} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span>{poll.votesCount} votes</span>
            </div>
          )}
        </div>

        <div className={styles.actions}>
          {poll.status === 'active' && (
            <button
              onClick={() => onVote?.(poll.id)}
              className={`${styles.button} ${styles.buttonVote}`}
            >
              Vote
            </button>
          )}
          <button
            onClick={() => onView?.(poll.id)}
            className={`${styles.button} ${styles.buttonView}`}
          >
            {poll.status === 'active' ? 'Results' : 'View results'}
          </button>
        </div>
      </div>
    </div>
  );
}
