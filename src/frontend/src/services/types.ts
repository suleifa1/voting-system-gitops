export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  username: string;
}

export interface AuthResponse {
  token: string;
  user: {
    id: string;
    email: string;
    username: string;
  };
}

export interface User {
  id: string;
  email: string;
  username: string;
}

export interface ApiError {
  message: string;
  error?: string;
}

// ===== Survey Types =====

export interface QuestionOption {
  id: string;
  option_text: string;
  option_order: number;
}

export interface Question {
  id: string;
  question_text: string;
  question_order: number;
  allow_multiple_answers: boolean;
  options: QuestionOption[];
}

export interface Survey {
  id: string;
  title: string;
  description: string | null;
  status: 'draft' | 'active' | 'completed';
  created_at: string;
  end_date: string;
  responses_count: number;
  is_anonymous: boolean;
  questions?: Question[];
}

export interface SurveyListItem {
  id: string;
  title: string;
  description: string | null;
  status: 'draft' | 'active' | 'completed';
  created_at: string;
  end_date: string;
  responses_count: number;
  is_anonymous: boolean;
}

export interface AnswerSubmit {
  question_id: string;
  option_ids: string[];
}

export interface SurveyAnswersSubmit {
  survey_id: string;
  answers: AnswerSubmit[];
}

export interface SurveyStartResponse {
  survey_id: string;
  message: string;
  started_at: string;
}

export interface SurveyCompleteResponse {
  survey_id: string;
  message: string;
  completed_at: string;
}

export interface OptionResult {
  option_id: string;
  option_text: string;
  votes_count: number;
  percentage: number;
}

export interface QuestionResult {
  question_id: string;
  question_text: string;
  total_answers: number;
  options: OptionResult[];
}

export interface SurveyResults {
  survey_id: string;
  survey_title: string;
  total_responses: number;
  questions: QuestionResult[];
}