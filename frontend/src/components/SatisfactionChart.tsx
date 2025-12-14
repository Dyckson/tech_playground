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
        max: 10,
        ticks: {
          stepSize: 2,
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
            return `Score: ${value}/10`;
          },
        },
      },
    },
  };

  const scoreGeral = data?.score_geral || 0;
  const scoreColor = scoreGeral >= 8 ? '#4caf50' : scoreGeral >= 6 ? '#ff9800' : '#f44336';

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
            Score Geral (0-10)
          </Typography>
        </Box>
        <Box sx={{ height: 300 }}>
          <Radar data={chartData} options={options} />
        </Box>
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2, textAlign: 'center' }}>
          {data?.total_dimensoes || 0} dimensões avaliadas
        </Typography>
      </CardContent>
    </Card>
  );
};

export default SatisfactionChart;
