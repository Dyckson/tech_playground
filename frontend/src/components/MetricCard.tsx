import { Card, CardContent, Box, Typography } from '@mui/material';
import { 
  Groups as GroupsIcon, 
  SentimentSatisfied as SentimentIcon,
  TrendingUp as TrendingIcon,
  Business as BusinessIcon 
} from '@mui/icons-material';

interface MetricCardProps {
  title: string;
  value: number | string;
  icon: 'groups' | 'sentiment' | 'trending' | 'business';
  color?: string;
  subtitle?: string;
}

const iconMap = {
  groups: GroupsIcon,
  sentiment: SentimentIcon,
  trending: TrendingIcon,
  business: BusinessIcon,
};

export const MetricCard: React.FC<MetricCardProps> = ({ 
  title, 
  value, 
  icon, 
  color = 'primary.main',
  subtitle 
}) => {
  const Icon = iconMap[icon];

  return (
    <Card elevation={3} sx={{ height: '100%', borderTop: `4px solid ${color}` }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box 
            sx={{ 
              bgcolor: `${color}15`, 
              p: 1.5, 
              borderRadius: 2, 
              mr: 2 
            }}
          >
            <Icon sx={{ fontSize: 32, color }} />
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ flex: 1 }}>
            {title}
          </Typography>
        </Box>

        <Typography 
          variant="h3" 
          sx={{ fontWeight: 'bold', color, mb: subtitle ? 0.5 : 0 }}
        >
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

export default MetricCard;
