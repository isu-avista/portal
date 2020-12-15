// Checks local storage for user itme
// if there is a logged in user with token (jwt), return http
// authorization header. Otherwise, return an empty object
export default function authHeader() {
  const user = JSON.parse(localStorage.getItem('user'));

  if (user && user.token) {
    return { Authorization: `Bearer ${user.token}` };
  }
  return {};
}
