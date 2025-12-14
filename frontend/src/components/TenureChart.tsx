import { Box, Card, CardContent, Typography, CircularProgress } from '@mui/material';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { useTenureDistribution } from '../hooks/useCompanyMetrics';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const TenureChart = () => {
  const { data, isLoading, error } = useTenureDistribution();

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
          <Typography color="error">Erro ao carregar distribuição por tempo de casa</Typography>
        </CardContent>
      </Card>
    );
  }

  const distribuicao = data?.distribuicao || [];

  const chartData = {
    labels: distribuicao.map((item: any) => item.categoria),
    datasets: [
      {
        label: 'Funcionários',
        data: distribuicao.map((item: any) => item.quantidade),
        backgroundColor: '#1976d2',
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const value = context.parsed.y;
            const item = distribuicao[context.dataIndex];
            const percentage = item?.percentual || 0;
            return `${value} funcionários (${percentage}%)`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          precision: 0,
        },
      },
    },
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
          Distribuição por Tempo de Casa
        </Typography>
        <Box sx={{ height: 300 }}>
          <Bar data={chartData} options={options} />
        </Box>
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2, textAlign: 'center' }}>
          Total: {data?.total_funcionarios || 0} funcionários
        </Typography>
      </CardContent>
    </Card>
  );
};

export default TenureChart;
