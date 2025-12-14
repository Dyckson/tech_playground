import { Card, CardContent, Box, Typography, Chip } from '@mui/material';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';
import { Radar } from 'react-chartjs-2';
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

interface ComparisonData {
  dimensao: string;
  employee_score: number | null;
  company_avg: number | null;
  area_avg: number | null;
  diff_company: number | null;
  diff_area: number | null;
}

interface EmployeeRadarComparisonProps {
  comparison: ComparisonData[];
  employeeName: string;
}

const EmployeeRadarComparison: React.FC<EmployeeRadarComparisonProps> = ({ comparison, employeeName }) => {
  const labels = comparison.map((item) => item.dimensao);
  
  const chartData = {
    labels,
    datasets: [
      {
        label: employeeName,
        data: comparison.map((item) => item.employee_score || 0),
        backgroundColor: 'rgba(25, 118, 210, 0.2)',
        borderColor: '#1976d2',
        borderWidth: 2,
        pointBackgroundColor: '#1976d2',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#1976d2',
      },
      {
        label: 'Média da Empresa',
        data: comparison.map((item) => item.company_avg || 0),
        backgroundColor: 'rgba(76, 175, 80, 0.2)',
        borderColor: '#4caf50',
        borderWidth: 2,
        pointBackgroundColor: '#4caf50',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#4caf50',
      },
      {
        label: 'Média da Área',
        data: comparison.map((item) => item.area_avg || 0),
        backgroundColor: 'rgba(255, 152, 0, 0.2)',
        borderColor: '#ff9800',
        borderWidth: 2,
        pointBackgroundColor: '#ff9800',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#ff9800',
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
        position: 'top' as const,
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const label = context.dataset.label || '';
            const value = context.parsed.r?.toFixed(2) || '0.00';
            return `${label}: ${value}`;
          },
        },
      },
    },
  };

  // Calcular estatísticas gerais
  const avgEmployeeScore = comparison.reduce((acc, item) => acc + (item.employee_score || 0), 0) / comparison.length;
  const avgCompanyScore = comparison.reduce((acc, item) => acc + (item.company_avg || 0), 0) / comparison.length;
  const overallDiff = avgEmployeeScore - avgCompanyScore;

  const getTrendIcon = (diff: number | null) => {
    if (!diff) return <TrendingFlat fontSize="small" />;
    if (diff > 0.5) return <TrendingUp fontSize="small" color="success" />;
    if (diff < -0.5) return <TrendingDown fontSize="small" color="error" />;
    return <TrendingFlat fontSize="small" color="warning" />;
  };

  const getTrendColor = (diff: number | null) => {
    if (!diff) return 'default';
    if (diff > 0.5) return 'success';
    if (diff < -0.5) return 'error';
    return 'warning';
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
          Comparação de Desempenho
        </Typography>

        <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
          <Chip
            icon={getTrendIcon(overallDiff)}
            label={`Diferença Geral: ${overallDiff > 0 ? '+' : ''}${overallDiff.toFixed(2)}`}
            color={getTrendColor(overallDiff) as any}
            size="small"
          />
          <Chip
            label={`Média Funcionário: ${avgEmployeeScore.toFixed(2)}`}
            color="primary"
            size="small"
            variant="outlined"
          />
          <Chip
            label={`Média Empresa: ${avgCompanyScore.toFixed(2)}`}
            color="success"
            size="small"
            variant="outlined"
          />
        </Box>

        <Box sx={{ height: 400 }}>
          <Radar data={chartData} options={options} />
        </Box>

        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2, textAlign: 'center' }}>
          {comparison.length} dimensões avaliadas
        </Typography>
      </CardContent>
    </Card>
  );
};

export default EmployeeRadarComparison;
