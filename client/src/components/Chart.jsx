import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top",
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1,
      },
      title: {
        display: true,
        text: "Container Status (Off/On)",
      },
    },
    x: {
      beginAtZero: false,
      title: {
        display: true,
        text: "Time (hh:mm)",
      },
    },
  },
};

export default function Chart({ inView }) {
  const data = {
    labels: inView.labels,
    datasets: [
      {
        label: inView.key,
        data: inView.performance,
        borderColor: "hsl(257, 81%, 55%)",
        backgroundColor: "white",
      },
    ],
  };
  return <Line options={options} data={data} />;
}
