import { Box, Card, CardContent, Typography, CircularProgress } from '@mui/material';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { useEnps } from '../hooks/useCompanyMetrics';

ChartJS.register(ArcElement, Tooltip, Legend);

const EnpsChart = () => {
  const { data, isLoading, error } = useEnps();

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
          <Typography color="error">Erro ao carregar dados eNPS</Typography>
        </CardContent>
      </Card>
    );
  }

  const chartData = {
    labels: ['Promotores', 'Neutros', 'Detratores'],
    datasets: [
      {
        data: [data?.promotores || 0, data?.neutros || 0, data?.detratores || 0],
        backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
        borderWidth: 2,
        borderColor: '#fff',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const label = context.label || '';
            const value = context.parsed || 0;
            const dataset = context.dataset.data;
            const total = dataset.reduce((acc: number, val: number) => acc + val, 0);
            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
            return `${label}: ${value} (${percentage}%)`;
          },
        },
      },
    },
  };

  const enpsScore = data?.enps_score || 0;
  const scoreColor = enpsScore >= 50 ? '#4caf50' : enpsScore >= 0 ? '#ff9800' : '#f44336';

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
          Distribuição eNPS
        </Typography>
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Typography variant="h3" sx={{ fontWeight: 'bold', color: scoreColor }}>
            {enpsScore > 0 ? '+' : ''}{enpsScore}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            eNPS Score
          </Typography>
        </Box>
        <Box sx={{ height: 250 }}>
          <Pie data={chartData} options={options} />
        </Box>
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2, textAlign: 'center' }}>
          Total: {data?.total_respostas || 0} respostas
        </Typography>
      </CardContent>
    </Card>
  );
};

export default EnpsChart;
