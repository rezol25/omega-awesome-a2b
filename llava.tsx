// src/pages/models/llava.tsx
import { NextPage } from 'next';
import { ModelLayout } from '../../components/layouts/ModelLayout';
import { LLaVAInterface } from '../../components/models/LLaVAInterface';

const LLaVAPage: NextPage = () => {
  return (
    <ModelLayout
      title="LLaVA Visual Assistant"
      description="Large Language and Vision Assistant"
    >
      <LLaVAInterface />
    </ModelLayout>
  );
};

export default LLaVAPage;
