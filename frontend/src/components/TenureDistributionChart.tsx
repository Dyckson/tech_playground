import { Card, CardHeader, CardContent, CircularProgress, Alert, Box, Typography } from '@mui/material';
import { Schedule as ScheduleIcon } from '@mui/icons-material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import type { TenureDistribution } from '@/types/api.types';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface TenureDistributionChartProps {
  data: TenureDistribution;
  isLoading?: boolean;
  error?: Error | null;
}

const TenureDistributionChart: React.FC<TenureDistributionChartProps> = ({
  data,
  isLoading,
  error,
}) => {
  if (isLoading) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent sx={{ textAlign: 'center', py: 5 }}>
          <CircularProgress />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
            Carregando distribuição de tempo...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Alert severity="error">Erro ao carregar dados: {error.message}</Alert>
        </CardContent>
      </Card>
    );
  }

  const chartData = {
    labels: ['< 1 ano', '1-2 anos', '3-5 anos', '5-10 anos', '> 10 anos'],
    datasets: [
      {
        label: 'Número de Funcionários',
        data: [
          data.lessThan1Year,
          data.oneToTwoYears,
          data.threeToFiveYears,
          data.fiveToTenYears,
          data.moreThan10Years,
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(153, 102, 255, 0.8)',
          'rgba(255, 159, 64, 0.8)',
          'rgba(255, 99, 132, 0.8)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(255, 99, 132, 1)',
        ],
        borderWidth: 2,
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
            const value = context.parsed.y || 0;
            const total = Object.values(data).reduce((acc, val) => acc + val, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${value} funcionários (${percentage}%)`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <Card elevation={2} sx={{ height: '100%' }}>
      <CardHeader
        avatar={<ScheduleIcon />}
        title="Distribuição por Tempo de Casa"
        titleTypographyProps={{ variant: 'h6' }}
      />
      <CardContent>
        <Box sx={{ height: 350 }}>
          <Bar data={chartData} options={options} />
        </Box>
      </CardContent>
    </Card>
  );
};

export default TenureDistributionChart;
