module.exports = {
  testEnvironment: 'jsdom',
  setupFiles: ['jest-chrome/setup.js'],
  moduleFileExtensions: ['js', 'jsx'],
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
  },
  verbose: true,
};