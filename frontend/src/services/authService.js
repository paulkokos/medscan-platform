import api from './api';

/**
 * Login user with email and password
 * @param {Object} credentials - { email, password }
 * @returns {Promise} - { token, user }
 */
export const login = async (credentials) => {
  const response = await api.post('/auth/login/', credentials);
  return response.data;
};

/**
 * Register new user
 * @param {Object} userData - { email, password, first_name, last_name }
 * @returns {Promise} - { token, user }
 */
export const register = async (userData) => {
  const response = await api.post('/auth/register/', userData);
  return response.data;
};

/**
 * Logout current user
 * @returns {Promise}
 */
export const logout = async () => {
  const response = await api.post('/auth/logout/');
  return response.data;
};

/**
 * Get current user profile
 * @returns {Promise} - User object
 */
export const getCurrentUser = async () => {
  const response = await api.get('/auth/user/');
  return response.data;
};

/**
 * Update user profile
 * @param {Object} userData - User data to update
 * @returns {Promise} - Updated user object
 */
export const updateProfile = async (userData) => {
  const response = await api.patch('/auth/user/', userData);
  return response.data;
};

/**
 * Change user password
 * @param {Object} passwords - { old_password, new_password }
 * @returns {Promise}
 */
export const changePassword = async (passwords) => {
  const response = await api.post('/auth/change-password/', passwords);
  return response.data;
};

/**
 * Request password reset
 * @param {string} email - User email
 * @returns {Promise}
 */
export const requestPasswordReset = async (email) => {
  const response = await api.post('/auth/password-reset/', { email });
  return response.data;
};

/**
 * Confirm password reset
 * @param {Object} data - { token, password }
 * @returns {Promise}
 */
export const confirmPasswordReset = async (data) => {
  const response = await api.post('/auth/password-reset-confirm/', data);
  return response.data;
};
