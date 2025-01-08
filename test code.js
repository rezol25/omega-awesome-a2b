import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import EmotiVoiceInterface from './EmotiVoiceInterface'; // Adjust the import path based on your project structure
import { useModelInference } from '../hooks/useModelInference'; // Mock this hook

jest.mock('../hooks/useModelInference'); // Mock the custom hook to test the component independently

describe('EmotiVoiceInterface', () => {

    beforeEach(() => {
        // Reset any mocks before each test
        useModelInference.mockClear();
    });

    // Basic Text-to-Speech Test
    it('should generate audio for basic text-to-speech', async () => {
        useModelInference.mockReturnValue({
            runInference: jest.fn().mockResolvedValue({ audioUrl: 'test-audio-url' })
        });

        render(<EmotiVoiceInterface />);

        fireEvent.change(screen.getByPlaceholderText('Enter text to convert to emotional speech...'), {
            target: { value: "Hello, this is a test message" }
        });

        fireEvent.click(screen.getByText('Generate Speech'));

        await waitFor(() => expect(screen.getByText('Click to play')).toBeInTheDocument());

        expect(useModelInference).toHaveBeenCalledWith('mistral');
        expect(screen.getByText('Click to play')).toBeInTheDocument();
    });

    // Emotion Variation Test
    it('should handle emotion variation correctly', async () => {
        useModelInference.mockReturnValue({
            runInference: jest.fn().mockResolvedValue({ audioUrl: 'exciting-audio-url' })
        });

        render(<EmotiVoiceInterface />);

        fireEvent.change(screen.getByPlaceholderText('Enter text to convert to emotional speech...'), {
            target: { value: "This is very exciting news!" }
        });

        fireEvent.change(screen.getByLabelText('Emotion'), { target: { value: 'excited' } });
        fireEvent.change(screen.getByLabelText('Emotion Intensity'), { target: { value: 0.8 } });

        fireEvent.click(screen.getByText('Generate Speech'));

        await waitFor(() => expect(screen.getByText('Click to play')).toBeInTheDocument());

        expect(useModelInference).toHaveBeenCalledWith('mistral');
        expect(screen.getByText('Click to play')).toBeInTheDocument();
    });

    // Edge Case Tests
    it('should handle empty text input gracefully', async () => {
        useModelInference.mockReturnValue({
            runInference: jest.fn().mockResolvedValue({ audioUrl: '' })
        });

        render(<EmotiVoiceInterface />);

        fireEvent.change(screen.getByPlaceholderText('Enter text to convert to emotional speech...'), {
            target: { value: '' }
        });

        fireEvent.click(screen.getByText('Generate Speech'));

        await waitFor(() => expect(screen.queryByText('Click to play')).not.toBeInTheDocument());
        expect(screen.getByText('Generate Speech')).toBeDisabled();
    });

    it('should handle very long text input without issues', async () => {
        useModelInference.mockReturnValue({
            runInference: jest.fn().mockResolvedValue({ audioUrl: 'long-text-audio-url' })
        });

        render(<EmotiVoiceInterface />);

        const longText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ".repeat(10); // Make it long
        fireEvent.change(screen.getByPlaceholderText('Enter text to convert to emotional speech...'), {
            target: { value: longText }
        });

        fireEvent.click(screen.getByText('Generate Speech'));

        await waitFor(() => expect(screen.getByText('Click to play')).toBeInTheDocument());
        expect(screen.getByText('Click to play')).toBeInTheDocument();
    });

});
