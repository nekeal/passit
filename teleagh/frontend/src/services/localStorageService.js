
function setTokens(tokens) {
  localStorage.setItem('access-token', tokens.access);
  localStorage.setItem('refresh-token', tokens.refresh);
}

function removeTokens() {
  localStorage.removeItem('access-token');
  localStorage.removeItem('refresh-token');
}

export default { setTokens, removeTokens };
