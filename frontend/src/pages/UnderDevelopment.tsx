import { Box, Alert, AlertTitle, Typography, Paper, Chip } from '@mui/material';
import { Construction as ConstructionIcon, Code as CodeIcon } from '@mui/icons-material';

interface UnderDevelopmentProps {
  feature: string;
  requiredEndpoint: string;
  description?: string;
}

export const UnderDevelopment: React.FC<UnderDevelopmentProps> = ({ 
  feature, 
  requiredEndpoint,
  description 
}) => {
  return (
    <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
      <Alert 
        severity="warning" 
        icon={<ConstructionIcon fontSize="large" />}
        sx={{ mb: 2 }}
      >
        <AlertTitle sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}>
          🚧 Funcionalidade em Desenvolvimento
        </AlertTitle>
        <Typography variant="body1" sx={{ mb: 2 }}>
          A funcionalidade <strong>"{feature}"</strong> está em desenvolvimento e será implementada em breve.
        </Typography>
        
        {description && (
          <Typography variant="body2" sx={{ mb: 2, color: 'text.secondary' }}>
            {description}
          </Typography>
        )}

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 2 }}>
          <CodeIcon fontSize="small" />
          <Typography variant="body2" component="span" sx={{ fontWeight: 'medium' }}>
            Endpoint necessário:
          </Typography>
          <Chip 
            label={requiredEndpoint} 
            size="small" 
            color="warning"
            sx={{ fontFamily: 'monospace' }}
          />
        </Box>

        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
          💡 Este endpoint precisa ser implementado no backend FastAPI antes desta feature funcionar.
        </Typography>
      </Alert>

      <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
        <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 'bold' }}>
          Status do Backend:
        </Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>
          ✅ Backend rodando em <code>http://localhost:9876/api/v1</code>
          <br />
          ✅ Banco PostgreSQL com 519 funcionários
          <br />
          ⏳ Endpoints de analytics pendentes
        </Typography>
      </Box>
    </Paper>
  );
};

export default UnderDevelopment;
