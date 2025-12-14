import { Card, CardHeader, CardContent, Grid, Box, Typography, CircularProgress } from '@mui/material';
import { Business as BusinessIcon, Group as GroupIcon, TrendingUp as TrendingUpIcon, Star as StarIcon, Assessment as AssessmentIcon } from '@mui/icons-material';
import type { CompanyMetrics } from '@/types/api.types';

interface CompanyOverviewProps {
  metrics: CompanyMetrics;
  isLoading?: boolean;
}

const CompanyOverview: React.FC<CompanyOverviewProps> = ({ metrics, isLoading }) => {
  if (isLoading) {
    return (
      <Card>
        <CardContent sx={{ textAlign: 'center', py: 5 }}>
          <CircularProgress />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
            Carregando métricas...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  const metricCards = [
    {
      title: 'Total de Funcionários',
      value: metrics.totalFuncionarios.toLocaleString('pt-BR'),
      icon: <GroupIcon fontSize="large" />,
      color: 'primary.main',
    },
    {
      title: 'eNPS Médio',
      value: metrics.enpsAverage.toFixed(1),
      icon: <AssessmentIcon fontSize="large" />,
      color: 'success.main',
      subtitle: 'Score: -100 a +100',
    },
    {
      title: 'Satisfação Média',
      value: `${metrics.satisfactionAverage.toFixed(1)}/7`,
      icon: <StarIcon fontSize="large" />,
      color: 'info.main',
    },
    {
      title: 'Taxa de Resposta',
      value: `${metrics.responseRate}%`,
      icon: <TrendingUpIcon fontSize="large" />,
      color: 'warning.main',
    },
  ];

  return (
    <Card elevation={2}>
      <CardHeader
        avatar={<BusinessIcon />}
        title="Visão Geral da Empresa"
        sx={{ bgcolor: 'primary.main', color: 'white' }}
      />
      <CardContent>
        <Grid container spacing={3}>
          {metricCards.map((metric, index) => (
            <Grid item xs={6} md={3} key={index}>
              <Card variant="outlined" sx={{ height: '100%', borderColor: metric.color, borderWidth: 2 }}>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Box sx={{ color: metric.color, mb: 2 }}>
                    {metric.icon}
                  </Box>
                  <Typography variant="caption" color="text.secondary" gutterBottom>
                    {metric.title}
                  </Typography>
                  <Typography variant="h4" sx={{ color: metric.color, fontWeight: 'bold' }}>
                    {metric.value}
                  </Typography>
                  {metric.subtitle && (
                    <Typography variant="caption" color="text.secondary">
                      {metric.subtitle}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default CompanyOverview;
