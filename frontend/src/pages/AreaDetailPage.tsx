import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Breadcrumbs,
  Link,
  Chip,
  CircularProgress,
  Alert,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  NavigateNext as NavigateNextIcon,
  TrendingUp as TrendingUpIcon,
  People as PeopleIcon,
  SentimentSatisfied as SentimentIcon,
  ArrowBack as ArrowBackIcon,
} from '@mui/icons-material';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, ArcElement } from 'chart.js';
import { Radar, Pie } from 'react-chartjs-2';
import TabNavigation from '../components/TabNavigation';
import { useAreaDetails, useAreaMetrics } from '../hooks/useAreas';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend, ArcElement);

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
  subtitle?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, icon, color, subtitle }) => {
  return (
    <Card elevation={3} sx={{ height: '100%', borderTop: `4px solid ${color}` }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ bgcolor: `${color}15`, p: 1.5, borderRadius: 2, mr: 2 }}>
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

const AreaDetailPage: React.FC = () => {
  const { id: areaId } = useParams<{ id: string }>();
  const navigate = useNavigate();

  console.log('🆔 Area ID da URL:', areaId);

  const { data: areaDetails, isLoading: detailsLoading, error: detailsError } = useAreaDetails(areaId);
  const { data: metrics, isLoading: metricsLoading } = useAreaMetrics(areaId);

  // Buscar funcionários da área
  const { data: funcionariosData } = useQuery({
    queryKey: ['areaFuncionarios', areaId],
    queryFn: async () => {
      const { data } = await axios.get('http://localhost:9876/api/v1/funcionarios', {
        params: {
          areas: [areaId],
          page: 1,
          page_size: 100,
          order_by: 'score',
          order_dir: 'desc',
        },
        paramsSerializer: { indexes: null },
      });
      return data;
    },
    enabled: !!areaId,
  });

  // Buscar scores por dimensão da área
  const { data: dimensoesData } = useQuery({
    queryKey: ['areaDimensoes', areaId],
    queryFn: async () => {
      const { data } = await axios.get('http://localhost:9876/api/v1/analytics/satisfaction-scores');
      return data;
    },
    enabled: !!areaId,
  });

  const isLoading = detailsLoading || metricsLoading;

  if (detailsError) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <TabNavigation />
        <Alert severity="error" sx={{ mt: 3 }}>
          Erro ao carregar detalhes da área
        </Alert>
      </Container>
    );
  }

  if (isLoading) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <TabNavigation />
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
              Carregando dados da área...
            </Typography>
          </Box>
        </Box>
      </Container>
    );
  }

  if (!areaDetails) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <TabNavigation />
        <Alert severity="warning" sx={{ mt: 3 }}>
          Área não encontrada
        </Alert>
      </Container>
    );
  }

  const funcionarios = funcionariosData?.items || [];
  const topPerformers = funcionarios.slice(0, 5);
  const bottomPerformers = [...funcionarios].reverse().slice(0, 5);

  // Calcular distribuição de cargos
  const cargoDistribution = new Map<string, number>();
  funcionarios.forEach((func: any) => {
    const cargo = func.cargo_nome || 'Sem cargo';
    cargoDistribution.set(cargo, (cargoDistribution.get(cargo) || 0) + 1);
  });

  const cargoChartData = {
    labels: Array.from(cargoDistribution.keys()),
    datasets: [
      {
        data: Array.from(cargoDistribution.values()),
        backgroundColor: [
          '#1976d2',
          '#2e7d32',
          '#ed6c02',
          '#9c27b0',
          '#d32f2f',
          '#0288d1',
          '#388e3c',
          '#f57c00',
        ],
        borderWidth: 2,
        borderColor: '#fff',
      },
    ],
  };

  // Gráfico radar de dimensões
  const dimensoes = dimensoesData?.dimensoes || [];
  const radarData = {
    labels: dimensoes.map((d: any) => d.dimensao),
    datasets: [
      {
        label: areaDetails.area,
        data: dimensoes.map((d: any) => d.score_medio || 0),
        backgroundColor: 'rgba(25, 118, 210, 0.2)',
        borderColor: '#1976d2',
        borderWidth: 2,
        pointBackgroundColor: '#1976d2',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#1976d2',
      },
    ],
  };

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        beginAtZero: true,
        max: 7,
        ticks: { stepSize: 1 },
      },
    },
    plugins: {
      legend: { display: false },
    },
  };

  const enpsScore = metrics?.enps_score ?? null;
  const enpsColor = enpsScore === null ? '#757575' : enpsScore >= 50 ? '#4caf50' : enpsScore >= 0 ? '#ff9800' : '#f44336';
  const scoreColor = metrics?.score_medio
    ? metrics.score_medio >= 6
      ? '#4caf50'
      : metrics.score_medio >= 5
      ? '#ff9800'
      : '#f44336'
    : '#757575';

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <TabNavigation />

      <Box sx={{ mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/areas')}
          sx={{ mb: 2 }}
        >
          Voltar para Áreas
        </Button>

        <Breadcrumbs separator={<NavigateNextIcon fontSize="small" />} sx={{ mb: 2 }}>
          <Link underline="hover" color="inherit" onClick={() => navigate('/')} sx={{ cursor: 'pointer' }}>
            {areaDetails.empresa}
          </Link>
          <Typography color="text.primary">{areaDetails.diretoria}</Typography>
          <Typography color="text.primary">{areaDetails.gerencia}</Typography>
          <Typography color="text.primary">{areaDetails.coordenacao}</Typography>
          <Typography color="primary.main" sx={{ fontWeight: 'bold' }}>
            {areaDetails.area}
          </Typography>
        </Breadcrumbs>

        <Typography variant="h3" sx={{ fontWeight: 'bold', mb: 1 }}>
          {areaDetails.area}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Perfil detalhado e métricas da área
        </Typography>
      </Box>

      {metrics?.total_funcionarios === 0 && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Esta área não possui funcionários cadastrados no momento.
        </Alert>
      )}

      {metrics && metrics.total_funcionarios > 0 && !metrics.score_medio && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          Os funcionários desta área ainda não possuem avaliações registradas. As métricas de eNPS e Satisfação serão calculadas assim que as avaliações forem concluídas.
        </Alert>
      )}

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Total de Funcionários"
            value={metrics?.total_funcionarios || 0}
            icon={<PeopleIcon sx={{ fontSize: 32, color: '#1976d2' }} />}
            color="#1976d2"
            subtitle="Colaboradores ativos"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="eNPS da Área"
            value={enpsScore !== null ? (enpsScore > 0 ? `+${enpsScore}` : enpsScore) : 'Calculando...'}
            icon={<SentimentIcon sx={{ fontSize: 32, color: enpsColor }} />}
            color={enpsColor}
            subtitle={
              metrics?.promotores || metrics?.detratores
                ? `${metrics?.promotores || 0} promotores / ${metrics?.detratores || 0} detratores`
                : 'Aguardando avaliações'
            }
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Satisfação Média"
            value={metrics?.score_medio ? metrics.score_medio.toFixed(2) : 'Calculando...'}
            icon={<TrendingUpIcon sx={{ fontSize: 32, color: scoreColor }} />}
            color={scoreColor}
            subtitle={metrics?.score_medio ? 'Score geral (1-7)' : 'Aguardando avaliações'}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Cargos Diferentes"
            value={cargoDistribution.size}
            icon={<PeopleIcon sx={{ fontSize: 32, color: '#9c27b0' }} />}
            color="#9c27b0"
            subtitle="Diversidade de funções"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Scores por Dimensão
              </Typography>
              <Box sx={{ height: 300 }}>
                {dimensoes.length > 0 ? (
                  <Radar data={radarData} options={radarOptions} />
                ) : (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <Typography color="text.secondary">Sem dados disponíveis</Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Distribuição de Cargos
              </Typography>
              <Box sx={{ height: 300 }}>
                {cargoDistribution.size > 0 ? (
                  <Pie
                    data={cargoChartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: { position: 'right' },
                      },
                    }}
                  />
                ) : (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <Typography color="text.secondary">Sem dados disponíveis</Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Top Performers
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Nome</TableCell>
                      <TableCell>Cargo</TableCell>
                      <TableCell align="center">Score</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {topPerformers.length > 0 ? (
                      topPerformers.map((func: any) => (
                        <TableRow
                          key={func.id}
                          hover
                          sx={{ cursor: 'pointer' }}
                          onClick={() => navigate(`/employees/${func.id}`)}
                        >
                          <TableCell>{func.nome}</TableCell>
                          <TableCell>{func.cargo_nome || 'N/A'}</TableCell>
                          <TableCell align="center">
                            <Chip
                              label={func.score_medio_geral?.toFixed(2) || 'N/A'}
                              size="small"
                              color={
                                func.score_medio_geral >= 6
                                  ? 'success'
                                  : func.score_medio_geral >= 5
                                  ? 'warning'
                                  : 'error'
                              }
                            />
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={3} align="center">
                          Sem dados
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
              <Box sx={{ mt: 2, textAlign: 'center' }}>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => navigate(`/employees?area=${areaId}`)}
                >
                  Ver Todos Funcionários
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Atenção Necessária
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Nome</TableCell>
                      <TableCell>Cargo</TableCell>
                      <TableCell align="center">Score</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {bottomPerformers.length > 0 ? (
                      bottomPerformers.map((func: any) => (
                        <TableRow
                          key={func.id}
                          hover
                          sx={{ cursor: 'pointer' }}
                          onClick={() => navigate(`/employees/${func.id}`)}
                        >
                          <TableCell>{func.nome}</TableCell>
                          <TableCell>{func.cargo_nome || 'N/A'}</TableCell>
                          <TableCell align="center">
                            <Chip
                              label={func.score_medio_geral?.toFixed(2) || 'N/A'}
                              size="small"
                              color={
                                func.score_medio_geral >= 6
                                  ? 'success'
                                  : func.score_medio_geral >= 5
                                  ? 'warning'
                                  : 'error'
                              }
                            />
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={3} align="center">
                          Sem dados
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AreaDetailPage;
