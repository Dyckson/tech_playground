import { Box, Card, CardContent, Grid, Typography, CircularProgress } from '@mui/material';
import {
  Business as BusinessIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  People as PeopleIcon,
} from '@mui/icons-material';
import { useAreas, useAreaEmployeeCount } from '../hooks/useAreas';

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
  subtitle?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, icon, color, subtitle }) => {
  return (
    <Card elevation={3} sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              bgcolor: `${color}15`,
              p: 1.5,
              borderRadius: 2,
              mr: 2,
            }}
          >
            {icon}
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ flex: 1 }}>
            {title}
          </Typography>
        </Box>

        <Typography variant="h3" sx={{ fontWeight: 'bold', color, mb: subtitle ? 0.5 : 0 }}>
          {value}
        </Typography>

        {subtitle && (
          <Typography variant="caption" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

interface AreaMetricsCardsProps {
  empresaId?: string;
}

const AreaMetricsCards: React.FC<AreaMetricsCardsProps> = ({ empresaId }) => {
  const { data: areas, isLoading: areasLoading } = useAreas(empresaId);
  const { data: contagem, isLoading: contagemLoading } = useAreaEmployeeCount(empresaId);

  if (areasLoading || contagemLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  // Calcular métricas
  const totalAreas = areas?.length || 0;
  
  const totalFuncionarios = contagem?.reduce((sum, item) => sum + item.total_funcionarios, 0) || 0;
  const mediaFuncionarios = totalAreas > 0 ? Math.round(totalFuncionarios / totalAreas) : 0;

  // Encontrar área com maior e menor quantidade de funcionários
  const areaMaior = contagem?.reduce((max, item) => 
    item.total_funcionarios > max.total_funcionarios ? item : max
  , contagem[0]);

  const areaMenor = contagem?.reduce((min, item) => 
    item.total_funcionarios < min.total_funcionarios ? item : min
  , contagem[0]);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <MetricCard
          title="Total de Áreas"
          value={totalAreas}
          icon={<BusinessIcon sx={{ fontSize: 32, color: '#1976d2' }} />}
          color="#1976d2"
          subtitle="Áreas ativas"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <MetricCard
          title="Média de Funcionários"
          value={mediaFuncionarios}
          icon={<PeopleIcon sx={{ fontSize: 32, color: '#2e7d32' }} />}
          color="#2e7d32"
          subtitle="Por área"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <MetricCard
          title="Área Mais Populosa"
          value={areaMaior?.total_funcionarios || 0}
          icon={<TrendingUpIcon sx={{ fontSize: 32, color: '#ed6c02' }} />}
          color="#ed6c02"
          subtitle={areaMaior?.area_nome || 'N/A'}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <MetricCard
          title="Área Menos Populosa"
          value={areaMenor?.total_funcionarios || 0}
          icon={<TrendingDownIcon sx={{ fontSize: 32, color: '#9c27b0' }} />}
          color="#9c27b0"
          subtitle={areaMenor?.area_nome || 'N/A'}
        />
      </Grid>
    </Grid>
  );
};

export default AreaMetricsCards;
