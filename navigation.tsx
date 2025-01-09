interface ModelMenuItem {
    id: string;
    label: string;
    icon: React.ReactNode;
    path: string;
    capabilities?: string[];
  }
  
  const modelMenuItems: ModelMenuItem[] = [
    // ... existing items
    {
      id: 'llava',
      label: 'LLaVA Visual Assistant',
      icon: <ModelIcon type="multimodal" />,
      path: '/models/llava',
      capabilities: ['image', 'text']
    }
  ];
  