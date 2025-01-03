// src/tests/BertModelInterface.test.jsx
import { render, fireEvent, waitFor } from '@testing-library/react';
import { BertModelInterface } from '../components/BertModelInterface';

describe('BertModelInterface', () => {
    it('handles input and submission correctly', async () => {
        const { getByPlaceholderText, getByText } = render(<BertModelInterface />);
        
        const input = getByPlaceholderText('Enter text for analysis...');
        fireEvent.change(input, { target: { value: 'Test input' } });
        
        const submitButton = getByText('Analyze');
        fireEvent.click(submitButton);
        
        await waitFor(() => {
            expect(getByText(/Results:/)).toBeInTheDocument();
        });
    });
});
