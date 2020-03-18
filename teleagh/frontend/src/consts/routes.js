const APP_ROUTES = {
  DASHBOARD: '/',
  LOGIN: '/login',
  SUBJECTS: '/subjects',
  SUBJECT: id => `/subjects/${id}`,
  EVENTS: '/events',
  PASSWORD_CHANGE: '/password-change',
  LECTURERS: '/lecturers',
  MEMES: '/memes',
  CONNECTION_PROBLEM: '/connection-problem'
};

const API_ROUTES = {
  JWT_CREATE: '/api/auth/jwt/create/',
  JWT_REFRESH: '/api/auth/jwt/refresh/',
  SET_PASSWORD: '/api/auth/users/set_password/',
  EVENTS: '/api/events/',
  NEWS: '/api/news/',
  SUBJECTS: semester => `/api/subjects/?semester=${semester}`,
  SUBJECT: id => `/api/subjects/${id}/`,
  RESOURCES: subjectId => `/api/resources/?subject=${subjectId}`,
  ME: '/api/auth/users/me/?expand=profile.field_age_groups.field_of_study',
  LECTURERS: '/api/lecturers/',
  SET_DEFAULT_FAG: '/api/auth/users/set_default_fag/'
};

export { APP_ROUTES, API_ROUTES };
