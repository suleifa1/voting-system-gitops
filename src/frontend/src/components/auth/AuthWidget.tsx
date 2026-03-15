'use client';

import { useState } from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

type AuthMode = 'login' | 'register';

interface AuthWidgetProps {
  onAuthSuccess?: () => void;
}

export default function AuthWidget({ onAuthSuccess }: AuthWidgetProps) {
  const [mode, setMode] = useState<AuthMode>('login');

  const handleAuthSuccess = () => {
    onAuthSuccess?.();
    window.location.href = '/dashboard';
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f5f5f5', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}>
      {mode === 'login' ? (
        <LoginForm
          onSuccess={handleAuthSuccess}
          onSwitchToRegister={() => setMode('register')}
        />
      ) : (
        <RegisterForm
          onSuccess={handleAuthSuccess}
          onSwitchToLogin={() => setMode('login')}
        />
      )}
    </div>
  );
}