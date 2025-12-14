import { Container, Grid, Box, Typography, CircularProgress, Alert, AlertTitle } from '@mui/material';
import { Dashboard as DashboardIcon } from '@mui/icons-material';
import MetricCard from '../components/MetricCard';
import EnpsChart from '../components/EnpsChart';
import TenureChart from '../components/TenureChart';
import SatisfactionChart from '../components/SatisfactionChart';
import TabNavigation from '../components/TabNavigation';
import { useEmployees, useEnps, useSatisfactionScores } from '../hooks/useCompanyMetrics';

const Dashboard: React.FC = () => {
  const { data: employeesData, isLoading, error } = useEmployees();
  const { data: enpsData } = useEnps();
  const { data: satisfactionData } = useSatisfactionScores();

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }} color="text.secondary">
            Carregando Dashboard...
          </Typography>
        </Box>
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Alert severity="error">
          <AlertTitle>Erro ao Carregar Dashboard</AlertTitle>
          Não foi possível conectar ao backend. Verifique se está rodando em http://localhost:9876
          <Box sx={{ mt: 2, fontFamily: 'monospace', fontSize: '0.875rem' }}>
            {(error as Error).message}
          </Box>
        </Alert>
      </Container>
    );
  }

  const totalFuncionarios = employeesData?.total || 0;

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <TabNavigation />
      
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
        <DashboardIcon sx={{ fontSize: 48, color: 'primary.main' }} />
        <Box>
          <Typography variant="h3" component="h1" sx={{ fontWeight: 'bold' }}>
            Dashboard Corporativo
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Visão geral de métricas e indicadores da empresa
          </Typography>
        </Box>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Total de Funcionários"
            value={totalFuncionarios.toLocaleString('pt-BR')}
            icon="groups"
            color="#1976d2"
            subtitle="Colaboradores ativos"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="eNPS Score"
            value={enpsData?.enps_score ? `${enpsData.enps_score > 0 ? '+' : ''}${enpsData.enps_score}` : '...'}
            icon="sentiment"
            color="#2e7d32"
            subtitle="Net Promoter Score"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Satisfação Média"
            value={satisfactionData?.score_geral ? satisfactionData.score_geral.toFixed(1) : '...'}
            icon="trending"
            color="#ed6c02"
            subtitle="Score médio geral"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Total Avaliações"
            value={enpsData?.total_respostas || '...'}
            icon="business"
            color="#9c27b0"
            subtitle="Respostas coletadas"
          />
        </Grid>
      </Grid>

      <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
        Análises e Visualizações
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={4}>
          <EnpsChart />
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <TenureChart />
        </Grid>
        <Grid item xs={12} md={12} lg={4}>
          <SatisfactionChart />
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
