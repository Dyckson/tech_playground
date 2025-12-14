import { Box, Card, CardContent, Typography, CircularProgress } from '@mui/material';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';
import { Radar } from 'react-chartjs-2';
import { useSatisfactionScores } from '../hooks/useCompanyMetrics';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const SatisfactionChart = () => {
  const { data, isLoading, error } = useSatisfactionScores();

  if (isLoading) {
    return (
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 300 }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card elevation={3}>
        <CardContent>
          <Typography color="error">Erro ao carregar scores de satisfação</Typography>
        </CardContent>
      </Card>
    );
  }

  const dimensoes = data?.dimensoes || [];

  const chartData = {
    labels: dimensoes.map((item: any) => item.dimensao),
    datasets: [
      {
        label: 'Score Médio',
        data: dimensoes.map((item: any) => item.score_medio || 0),
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

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        beginAtZero: true,
        max: 7,
        ticks: {
          stepSize: 1,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const value = context.parsed.r?.toFixed(2) || '0.00';
            return `Score: ${value}/7`;
          },
        },
      },
    },
  };

  const scoreGeral = data?.score_geral || 0;
  const scoreColor = scoreGeral >= 6 ? '#4caf50' : scoreGeral >= 5 ? '#ff9800' : '#f44336';

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
          Scores de Satisfação
        </Typography>
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Typography variant="h3" sx={{ fontWeight: 'bold', color: scoreColor }}>
            {scoreGeral.toFixed(2)}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Score Geral (1-7)
          </Typography>
        </Box>
        <Box sx={{ height: 300 }}>
          <Radar data={chartData} options={options} />
        </Box>
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Typography variant="caption" color="text.secondary" display="block">
            {data?.total_dimensoes || 0} dimensões avaliadas
          </Typography>
          <Typography variant="caption" color="text.secondary" display="block">
            Escala: 1 (Discordo totalmente) a 7 (Concordo totalmente)
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SatisfactionChart;
