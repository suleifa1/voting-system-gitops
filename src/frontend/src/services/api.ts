import axios from 'axios';
import {
  SurveyListItem,
  Survey,
  SurveyAnswersSubmit,
  SurveyStartResponse,
  SurveyCompleteResponse,
  SurveyResults,
} from './types';

// Используем пустую строку если NEXT_PUBLIC_API_URL не определен (для Ingress)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL !== undefined 
  ? process.env.NEXT_PUBLIC_API_URL 
  : 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

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
   * Get list of all surveys
   * @param statusFilter - filter by status (draft, active, completed)
   */
  async getSurveys(statusFilter?: string): Promise<SurveyListItem[]> {
    const params = statusFilter ? { status_filter: statusFilter } : {};
    const response = await api.get<SurveyListItem[]>('/surveys/', { params });
    return response.data;
  },

  /**
   * Get full survey with all questions
   * @param surveyId - survey ID
   */
  async getSurvey(surveyId: string): Promise<Survey> {
    const response = await api.get<Survey>(`/surveys/${surveyId}`);
    return response.data;
  },

  /**
   * Start survey (requires authentication)
   * @param surveyId - survey ID
   */
  async startSurvey(surveyId: string): Promise<SurveyStartResponse> {
    const response = await api.post<SurveyStartResponse>(`/surveys/${surveyId}/start`);
    return response.data;
  },

  /**
   * Submit survey answers (requires authentication)
   * @param surveyId - survey ID
   * @param answers - user answers
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
   * Get survey results
   * @param surveyId - survey ID
   */
  async getSurveyResults(surveyId: string): Promise<SurveyResults> {
    const response = await api.get<SurveyResults>(`/surveys/${surveyId}/results`);
    return response.data;
  },
};

export default api;