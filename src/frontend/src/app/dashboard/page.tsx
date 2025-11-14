'use client';

import { useEffect, useState } from 'react';
import { authService } from '@/services/auth';
import { User } from '@/services/types';
import PollsList from '@/components/polls/PollsList';
import styles from './page.module.css';

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          const userData = await authService.verify();
          setUser(userData);
        } else {
          window.location.href = '/';
        }
      } catch (error) {
        authService.logout();
        window.location.href = '/';
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogout = () => {
    authService.logout();
    window.location.href = '/';
  };

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.loadingContent}>
          <div className={styles.spinner}></div>
          <p className={styles.loadingText}>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <nav className={styles.nav}>
        <div className={styles.navContent}>
          <div className={styles.navInner}>
            <div className={styles.navLeft}>
              <h1 className={styles.title}>
                Voting System
              </h1>
            </div>
            <div className={styles.navRight}>
              <span className={styles.username}>Hello, {user?.username}!</span>
              <button
                onClick={handleLogout}
                className={styles.logoutButton}
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className={styles.main}>
        <div className={styles.content}>
          {/* Welcome */}
          <div className={styles.welcome}>
            <div className={styles.welcomeContent}>
              <h2 className={styles.welcomeTitle}>
                Welcome, {user?.username}! 👋
              </h2>
              <p className={styles.welcomeText}>
                Here you can view available surveys and vote in them.
              </p>
            </div>
          </div>

          {/* Surveys list */}
          <div className={styles.pollsSection}>
            <h3 className={styles.pollsTitle}>
              Available surveys
            </h3>
            <PollsList />
          </div>
        </div>
      </main>
    </div>
  );
}