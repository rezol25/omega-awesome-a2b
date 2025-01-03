// src/routes/ModelRoutes.jsx
import { Route, Routes } from 'react-router-dom';
import { BertModelInterface } from '../components/BertModelInterface';

export const ModelRoutes = () => {
    return (
        <Routes>
            <Route path="/models/bert" element={<BertModelInterface />} />
            {/* Other model routes */}
        </Routes>
    );
};
