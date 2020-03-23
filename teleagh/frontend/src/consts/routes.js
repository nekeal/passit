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
  NEWS: `/api/news/`,
  NEWS_FAG: fagId => `/api/news/?field_age_group=${fagId}`,
  NEWS_ITEM: id => `/api/news/${id}/`,
  SUBJECTS: (semester, fieldOfStudyId) => `/api/subjects/?semester=${semester}&field_of_study=${fieldOfStudyId}`,
  SUBJECT: id => `/api/subjects/${id}/`,
  RESOURCES: (subjectId, category) => `/api/resources/?subject=${subjectId}&category=${category}`,
  ME: '/api/auth/users/me/?expand=profile.field_age_groups.field_of_study,profile.memberships',
  LECTURERS: '/api/lecturers/',
  SET_DEFAULT_FAG: '/api/auth/users/set_default_fag/',
  SAGS: fagId => `/api/subjectsagegroup/?field_age_group=${fagId}&expand=subject_name`
};

export { APP_ROUTES, API_ROUTES };
