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

-- Tabela Professor_Turma (N:N)
CREATE TABLE IF NOT EXISTS professor_turma (
	id_professor INT NOT NULL REFERENCES professor(id_professor) ON DELETE CASCADE,
	id_turma INT NOT NULL REFERENCES turma(id_turma) ON DELETE CASCADE,
	PRIMARY KEY (id_professor, id_turma)
);

-- Tabela Material
CREATE TABLE IF NOT EXISTS material (
	id_material SERIAL PRIMARY KEY,
	id_turma INT NOT NULL REFERENCES turma(id_turma) ON DELETE CASCADE,
	id_professor INT NOT NULL REFERENCES professor(id_professor) ON DELETE CASCADE,
	titulo VARCHAR(255) NOT NULL
);