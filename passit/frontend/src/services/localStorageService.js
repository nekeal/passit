
function setTokens(tokens) {
  const { access, refresh } = tokens;
  access && localStorage.setItem('access-token', access);
  refresh && localStorage.setItem('refresh-token', refresh);
}

function getTokens() {
  return {
    access: localStorage.getItem('access-token'),
    refresh: localStorage.getItem('refresh-token')
  };
}

function removeTokens() {
  localStorage.removeItem('access-token');
  localStorage.removeItem('refresh-token');
}

function getSemester() {
  return localStorage.getItem("semester");
}

function setSemester(semester) {
  localStorage.setItem("semester", semester);
}

export default { setTokens, getTokens, removeTokens, getSemester, setSemester };
