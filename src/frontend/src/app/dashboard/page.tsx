'use client';

import { useEffect, useState } from 'react';
import { authService } from '@/services/auth';
import { User } from '@/services/types';

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
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Загрузка...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Система голосования
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Привет, {user?.username}!</span>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                Выйти
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Добро пожаловать в систему голосования!
              </h2>
              <p className="text-gray-600">
                Это MVP версия системы авторизации. Здесь будут отображаться опросы и возможность голосования.
              </p>
              
              <div className="mt-6 bg-blue-50 border border-blue-200 rounded-md p-4">
                <h3 className="text-sm font-medium text-blue-800">Информация о пользователе:</h3>
                <dl className="mt-2 text-sm text-blue-700">
                  <div>
                    <dt className="inline">ID: </dt>
                    <dd className="inline">{user?.id}</dd>
                  </div>
                  <div>
                    <dt className="inline">Email: </dt>
                    <dd className="inline">{user?.email}</dd>
                  </div>
                  <div>
                    <dt className="inline">Имя пользователя: </dt>
                    <dd className="inline">{user?.username}</dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}