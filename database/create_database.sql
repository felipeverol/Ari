-- Tabela Escola
CREATE TABLE IF NOT EXISTS escola (
    id_escola SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Tabela Turma
CREATE TABLE IF NOT EXISTS turma (
    id_turma SERIAL PRIMARY KEY,
    id_escola INT NOT NULL REFERENCES escola(id_escola) ON DELETE CASCADE,
    nome VARCHAR(50) NOT NULL
);

-- Tabela Professor
CREATE TABLE IF NOT EXISTS professor (
    id_professor SERIAL PRIMARY KEY,
    id_escola INT NOT NULL REFERENCES escola(id_escola) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

-- Tabela Aluno
CREATE TABLE IF NOT EXISTS aluno (
    id_aluno SERIAL PRIMARY KEY,
    id_turma INT NOT NULL REFERENCES turma(id_turma) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

-- Tabela Disciplina
CREATE TABLE IF NOT EXISTS disciplina (
    id_disciplina SERIAL PRIMARY KEY,
    id_turma INT NOT NULL REFERENCES turma(id_turma) ON DELETE CASCADE,
    id_professor INT NOT NULL REFERENCES professor(id_professor) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL
);

-- Tabela Material
CREATE TABLE IF NOT EXISTS material (
    id_material SERIAL PRIMARY KEY,
    id_disciplina INT NOT NULL REFERENCES disciplina(id_disciplina) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL
);