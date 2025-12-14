import { Card, CardHeader, CardContent, CircularProgress, Alert, Box, Typography } from '@mui/material';
import { PieChart as PieChartIcon } from '@mui/icons-material';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import type { EnpsDistribution } from '@/types/api.types';

ChartJS.register(ArcElement, Tooltip, Legend);

interface EnpsDistributionChartProps {
  data: EnpsDistribution;
  isLoading?: boolean;
  error?: Error | null;
}

const EnpsDistributionChart: React.FC<EnpsDistributionChartProps> = ({
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
            Carregando distribuição eNPS...
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
    labels: ['Promotores (9-10)', 'Passivos (7-8)', 'Detratores (0-6)'],
    datasets: [
      {
        data: [data.promoters, data.passives, data.detractors],
        backgroundColor: [
          'rgba(40, 167, 69, 0.8)',   // Green
          'rgba(255, 193, 7, 0.8)',    // Yellow
          'rgba(220, 53, 69, 0.8)',    // Red
        ],
        borderColor: [
          'rgba(40, 167, 69, 1)',
          'rgba(255, 193, 7, 1)',
          'rgba(220, 53, 69, 1)',
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
        position: 'bottom' as const,
        labels: {
          padding: 15,
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = data.promoters + data.passives + data.detractors;
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: ${value} (${percentage}%)`;
          },
        },
      },
    },
  };

  const scoreColor = data.score >= 50 ? 'success.main' : data.score >= 0 ? 'warning.main' : 'error.main';

  return (
    <Card elevation={2} sx={{ height: '100%' }}>
      <CardHeader
        avatar={<PieChartIcon />}
        title="Distribuição eNPS"
        titleTypographyProps={{ variant: 'h6' }}
      />
      <CardContent>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h2" sx={{ color: scoreColor, fontWeight: 'bold' }}>
            {data.score}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Net Promoter Score
          </Typography>
        </Box>
        <Box sx={{ height: 300 }}>
          <Doughnut data={chartData} options={options} />
        </Box>
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            eNPS = % Promotores - % Detratores
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default EnpsDistributionChart;
