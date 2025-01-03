// src/components/Navigation.jsx
import { Link } from 'react-router-dom';

export const Navigation = () => {
    return (
        <nav>
            <Link to="/models/bert">BERT Model</Link>
            {/* Other navigation items */}
        </nav>
    );
};
