import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/Medical Text Summarization/i);
  expect(headingElement).toBeInTheDocument();
});
