<script setup>
import { onMounted, ref } from 'vue'
import { tccApi } from '../services/tccApi'

const statusOptions = [
  { value: '0', label: 'Em Elaboração' },
  { value: '1', label: 'Enviado' },
  { value: '2', label: 'Aprovado' },
  { value: '3', label: 'Reprovado' },
]

const tccs = ref([])
const alunos = ref([])
const professores = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const feedbackMessage = ref('')
const feedbackType = ref('')
const updatingId = ref(null)
const searchQuery = ref('')

function getAlunoNome(alunoId) {
  const a = alunos.value.find(a => a.id === alunoId)
  return a ? a.nome : `#${alunoId}`
}

function getProfessorNome(profId) {
  const p = professores.value.find(p => p.id === profId)
  return p ? p.nome : `#${profId}`
}

async function loadAll() {
  isLoading.value = true
  errorMessage.value = ''
  feedbackMessage.value = ''
  try {
    const params = {}
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }
    const [tccRes, alunosRes, profsRes] = await Promise.all([
      tccApi.getTccs(params),
      tccApi.getStudents(),
      tccApi.getProfessors(),
    ])
    tccs.value = tccRes.data
    alunos.value = alunosRes.data
    professores.value = profsRes.data
  } catch (error) {
    errorMessage.value = 'Não foi possível carregar os TCCs. Verifique se o backend está rodando.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

async function updateStatus(tcc) {
  updatingId.value = tcc.id
  feedbackMessage.value = ''
  try {
    const response = await tccApi.patchTcc(tcc.id, { status: tcc.status })
    const idx = tccs.value.findIndex(t => t.id === tcc.id)
    if (idx !== -1) {
      tccs.value[idx] = response.data
    }
    feedbackMessage.value = 'Status alterado com sucesso!'
    feedbackType.value = 'success'
  } catch (error) {
    feedbackMessage.value = 'Erro ao alterar status.'
    feedbackType.value = 'error'
    console.error(error)
  } finally {
    updatingId.value = null
    setTimeout(() => {
      feedbackMessage.value = ''
    }, 3000)
  }
}

onMounted(loadAll)
</script>

<template>
  <section class="page">
    <header class="page-header">
      <div>
        <h1>TCCs</h1>
        <p>Listagem, busca, cadastro e alteração de status dos TCCs.</p>
      </div>
    </header>

    <div v-if="feedbackMessage" :class="['status-box', feedbackType === 'error' ? 'status-box-error' : '']">
      {{ feedbackMessage }}
    </div>

    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar por título ou resumo..."
        @keyup.enter="loadAll"
      />
      <button type="button" class="button-secondary" @click="loadAll">
        Buscar
      </button>
    </div>

    <div v-if="isLoading" class="status-box">
      Carregando TCCs...
    </div>

    <div v-else-if="errorMessage" class="status-box status-box-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="tccs.length === 0" class="status-box">
      Nenhum TCC encontrado.
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Aluno</th>
            <th>Orientador</th>
            <th>Tipo</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tcc in tccs" :key="tcc.id">
            <td>{{ tcc.titulo }}</td>
            <td>{{ getAlunoNome(tcc.aluno) }}</td>
            <td>{{ getProfessorNome(tcc.orientador) }}</td>
            <td>{{ tcc.tipo_display }}</td>
            <td>
              <select
                v-model="tcc.status"
                :disabled="updatingId === tcc.id"
                @change="updateStatus(tcc)"
              >
                <option
                  v-for="opt in statusOptions"
                  :key="opt.value"
                  :value="opt.value"
                >
                  {{ opt.label }}
                </option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.search-bar {
  display: flex;
  gap: 8px;
}

.search-bar input {
  flex: 1;
  border: 1px solid #c9d4e5;
  border-radius: 8px;
  padding: 10px 14px;
  background: #ffffff;
  font: inherit;
}

.table-container {
  border: 1px solid #dfe5ee;
  border-radius: 8px;
  background: #ffffff;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 12px 16px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #667085;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #edf1f7;
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid #edf1f7;
  color: #17202a;
}

tr:last-child td {
  border-bottom: 0;
}

td select {
  border: 1px solid #c9d4e5;
  border-radius: 6px;
  padding: 6px 10px;
  background: #ffffff;
  color: #17202a;
  cursor: pointer;
  font: inherit;
}

td select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
