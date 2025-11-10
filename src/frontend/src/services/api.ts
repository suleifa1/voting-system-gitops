import axios from 'axios';
import {
  SurveyListItem,
  Survey,
  SurveyAnswersSubmit,
  SurveyStartResponse,
  SurveyCompleteResponse,
  SurveyResults,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем токен к каждому запросу если он есть
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Перехватываем ответы для обработки ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ===== Survey API Methods =====

export const surveyApi = {
  /**
   * Получить список всех анкет
   * @param statusFilter - фильтр по статусу (draft, active, completed)
   */
  async getSurveys(statusFilter?: string): Promise<SurveyListItem[]> {
    const params = statusFilter ? { status_filter: statusFilter } : {};
    const response = await api.get<SurveyListItem[]>('/surveys/', { params });
    return response.data;
  },

  /**
   * Получить полную анкету со всеми вопросами
   * @param surveyId - ID анкеты
   */
  async getSurvey(surveyId: string): Promise<Survey> {
    const response = await api.get<Survey>(`/surveys/${surveyId}`);
    return response.data;
  },

  /**
   * Начать прохождение анкеты (требуется авторизация)
   * @param surveyId - ID анкеты
   */
  async startSurvey(surveyId: string): Promise<SurveyStartResponse> {
    const response = await api.post<SurveyStartResponse>(`/surveys/${surveyId}/start`);
    return response.data;
  },

  /**
   * Отправить ответы на анкету (требуется авторизация)
   * @param surveyId - ID анкеты
   * @param answers - ответы пользователя
   */
  async submitAnswers(
    surveyId: string,
    answers: SurveyAnswersSubmit
  ): Promise<SurveyCompleteResponse> {
    const response = await api.post<SurveyCompleteResponse>(
      `/surveys/${surveyId}/answer`,
      answers
    );
    return response.data;
  },

  /**
   * Получить результаты анкеты
   * @param surveyId - ID анкеты
   */
  async getSurveyResults(surveyId: string): Promise<SurveyResults> {
    const response = await api.get<SurveyResults>(`/surveys/${surveyId}/results`);
    return response.data;
  },
};

export default api;