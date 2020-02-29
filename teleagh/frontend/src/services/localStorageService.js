
function setTokens(tokens) {
  localStorage.setItem('access-token', tokens.access);
  localStorage.setItem('refresh-token', tokens.refresh);
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

export default { setTokens, getTokens, removeTokens };
