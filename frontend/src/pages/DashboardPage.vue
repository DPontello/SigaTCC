<script setup>
import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from 'chart.js'
import { computed, onMounted, ref } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import { tccApi } from '../services/tccApi'

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  Legend,
  LinearScale,
  Tooltip,
)

const isLoading = ref(true)
const errorMessage = ref('')
const statistics = ref(null)

const statusColors = ['#f5a524', '#1f66d1', '#2f9e44', '#d64545']
const typeColors = ['#1f66d1', '#5f6c7b', '#2f9e44', '#d97706']
const barColors = ['#1f66d1', '#2f9e44', '#d97706', '#7c3aed', '#d64545', '#0f766e']

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        boxWidth: 12,
        color: '#40566f',
        font: {
          size: 12,
          weight: '600',
        },
      },
    },
    tooltip: {
      backgroundColor: '#101828',
      padding: 10,
    },
  },
}

const barChartOptions = {
  ...chartOptions,
  scales: {
    x: {
      ticks: {
        color: '#607086',
      },
      grid: {
        display: false,
      },
    },
    y: {
      beginAtZero: true,
      ticks: {
        color: '#607086',
        precision: 0,
      },
      grid: {
        color: '#edf1f7',
      },
    },
  },
}

const totalTccs = computed(() => statistics.value?.total_geral ?? 0)

const approvedTccs = computed(() => {
  return statistics.value?.por_status?.Aprovado ?? 0
})

const sentTccs = computed(() => {
  return statistics.value?.por_status?.Enviado ?? 0
})

const activeOrientators = computed(() => {
  return Object.keys(statistics.value?.por_orientador ?? {}).length
})

const statusChartData = computed(() => {
  const data = statistics.value?.por_status ?? {}

  return {
    labels: Object.keys(data),
    datasets: [
      {
        data: Object.values(data),
        backgroundColor: statusColors,
        borderWidth: 0,
      },
    ],
  }
})

const typeChartData = computed(() => {
  const data = statistics.value?.por_tipo ?? {}

  return {
    labels: Object.keys(data),
    datasets: [
      {
        data: Object.values(data),
        backgroundColor: typeColors,
        borderWidth: 0,
      },
    ],
  }
})

const courseChartData = computed(() => {
  const data = statistics.value?.por_curso ?? {}

  return {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'TCCs',
        data: Object.values(data),
        backgroundColor: Object.keys(data).map(
          (_, index) => barColors[index % barColors.length],
        ),
        borderRadius: 6,
      },
    ],
  }
})

const semesterChartData = computed(() => {
  const data = statistics.value?.por_semestre ?? {}

  return {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'TCCs',
        data: Object.values(data),
        backgroundColor: '#1f66d1',
        borderRadius: 6,
      },
    ],
  }
})

async function loadStatistics() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await tccApi.getStatistics()
    statistics.value = response.data
  } catch (error) {
    errorMessage.value =
      'Não foi possível carregar as estatísticas. Confira se o backend Django está rodando em http://127.0.0.1:8000.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadStatistics)
</script>

<template>
  <section class="page">
    <header class="page-header">
      <div>
        <h1>Dashboard</h1>
        <p>Indicadores gerais dos trabalhos cadastrados.</p>
      </div>

      <button type="button" class="button-secondary" @click="loadStatistics">
        Atualizar
      </button>
    </header>

    <div v-if="isLoading" class="status-box">
      Carregando estatísticas...
    </div>

    <div v-else-if="errorMessage" class="status-box status-box-error">
      {{ errorMessage }}
    </div>

    <div v-else class="dashboard-content">
      <div class="metric-grid">
        <article class="metric-card">
          <span>Total de TCCs</span>
          <strong>{{ totalTccs }}</strong>
        </article>

        <article class="metric-card">
          <span>Aprovados</span>
          <strong>{{ approvedTccs }}</strong>
        </article>

        <article class="metric-card">
          <span>Enviados</span>
          <strong>{{ sentTccs }}</strong>
        </article>

        <article class="metric-card">
          <span>Orientadores ativos</span>
          <strong>{{ activeOrientators }}</strong>
        </article>
      </div>

      <div class="chart-grid">
        <article class="chart-panel">
          <h2>TCCs por status</h2>
          <div class="chart-box">
            <Doughnut :data="statusChartData" :options="chartOptions" />
          </div>
        </article>

        <article class="chart-panel">
          <h2>TCCs por tipo</h2>
          <div class="chart-box">
            <Doughnut :data="typeChartData" :options="chartOptions" />
          </div>
        </article>

        <article class="chart-panel chart-panel-wide">
          <h2>TCCs por curso</h2>
          <div class="chart-box chart-box-wide">
            <Bar :data="courseChartData" :options="barChartOptions" />
          </div>
        </article>

        <article class="chart-panel chart-panel-wide">
          <h2>TCCs por semestre</h2>
          <div class="chart-box chart-box-wide">
            <Bar :data="semesterChartData" :options="barChartOptions" />
          </div>
        </article>
      </div>
    </div>
  </section>
</template>