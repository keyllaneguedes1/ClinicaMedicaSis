CREATE DATABASE clinica_medica;

USE clinica_medica;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    senha VARCHAR(255),
    tipo ENUM('admin', 'recepcionista') NOT NULL
);

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    data_nascimento DATE,
    sexo ENUM('M', 'F'),
    telefone VARCHAR(20),
    endereco TEXT
);

CREATE TABLE medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    especialidade VARCHAR(100),
    crm VARCHAR(20) UNIQUE,
    telefone VARCHAR(20)
);

CREATE TABLE consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    id_medico INT,
    data_consulta DATETIME,
    observacoes TEXT,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id),
    FOREIGN KEY (id_medico) REFERENCES medicos(id)
);

CREATE TABLE exames (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT,
    tipo_exame VARCHAR(100),
    resultado TEXT,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id)
);

CREATE TABLE receitas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT,
    medicamento VARCHAR(100),
    posologia TEXT,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id)
);

CREATE TABLE log_consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT,
    data_log DATETIME DEFAULT CURRENT_TIMESTAMP,
    mensagem TEXT
);

DELIMITER //
CREATE TRIGGER trg_log_consulta_insert
AFTER INSERT ON consultas
FOR EACH ROW
BEGIN
    INSERT INTO log_consultas (id_consulta, mensagem)
    VALUES (NEW.id, CONCAT('Consulta cadastrada para o paciente ', NEW.id_paciente, ' com o médico ', NEW.id_medico));
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER trg_backup_paciente_delete
BEFORE DELETE ON pacientes
FOR EACH ROW
BEGIN
    INSERT INTO pacientes_backup
    SELECT * FROM pacientes WHERE id = OLD.id;
END;
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_historico_paciente (IN pid INT)
BEGIN
    SELECT 
        p.nome AS paciente,
        m.nome AS medico,
        c.data_consulta,
        c.observacoes,
        e.tipo_exame,
        e.resultado,
        r.medicamento,
        r.posologia
    FROM consultas c
    JOIN pacientes p ON c.id_paciente = p.id
    JOIN medicos m ON c.id_medico = m.id
    LEFT JOIN exames e ON e.id_consulta = c.id
    LEFT JOIN receitas r ON r.id_consulta = c.id
    WHERE p.id = pid;
END;
//
DELIMITER ;


CREATE VIEW vw_historico_pacientes AS
SELECT 
    p.id AS id_paciente,
    p.nome,
    c.data_consulta,
    m.nome AS medico,
    e.tipo_exame,
    r.medicamento
FROM pacientes p
LEFT JOIN consultas c ON c.id_paciente = p.id
LEFT JOIN medicos m ON c.id_medico = m.id
LEFT JOIN exames e ON e.id_consulta = c.id
LEFT JOIN receitas r ON r.id_consulta = c.id;

CREATE TABLE log_consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    id_medico INT,
    data_consulta DATETIME,
    acao VARCHAR(50),
    data_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


DELIMITER //

CREATE PROCEDURE sp_consultas_por_medico (
    IN mid INT,
    IN inicio DATE,
    IN fim DATE
)
BEGIN
    SELECT 
        c.id,
        p.nome AS nome_paciente,
        m.nome AS nome_medico,
        c.data_consulta,
        c.observacoes
    FROM consultas c
    JOIN pacientes p ON c.id_paciente = p.id
    JOIN medicos m ON c.id_medico = m.id
    WHERE c.id_medico = mid
      AND c.data_consulta BETWEEN inicio AND fim
    ORDER BY c.data_consulta;
END;
//

DELIMITER ;


CREATE VIEW vw_historico_pacientes AS
SELECT 
    p.id AS id_paciente,
    p.nome AS paciente,  
    c.data_consulta,
    m.nome AS medico,
    c.observacoes,
    e.tipo_exame,
    e.resultado,
    r.medicamento,
    r.posologia
FROM pacientes p
LEFT JOIN consultas c ON c.id_paciente = p.id
LEFT JOIN medicos m ON c.id_medico = m.id
LEFT JOIN exames e ON e.id_consulta = c.id
LEFT JOIN receitas r ON r.id_consulta = c.id;


USE clinica_medica;
CREATE TABLE pagamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    forma_pagamento ENUM('Dinheiro', 'Cartão', 'Pix', 'Convênio') NOT NULL,
    status_pagamento ENUM('Pendente', 'Pago', 'Cancelado') DEFAULT 'Pendente',
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id)
);

CREATE OR REPLACE VIEW vw_pagamentos_com_cliente AS
SELECT 
    p.id,
    p.id_consulta,
    p.valor,
    p.forma_pagamento,
    p.status_pagamento,
    p.data_pagamento,
    c.id_paciente,
    pac.nome AS nome_paciente
FROM pagamentos p
JOIN consultas c ON p.id_consulta = c.id
JOIN pacientes pac ON c.id_paciente = pac.id;

DELIMITER //
CREATE TRIGGER trg_pagamento_apos_inserir_consulta
AFTER INSERT ON consultas
FOR EACH ROW
BEGIN
    INSERT INTO pagamentos (
        id_consulta,
        valor,
        forma_pagamento,
        status_pagamento,
        data_pagamento
    ) VALUES (
        NEW.id,               
        0.00,                 
        'Dinheiro',           
        'Pendente',           
        NULL                  
    );
END;
//
DELIMITER ;

CREATE TABLE log_pagamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pagamento INT,
    acao ENUM('UPDATE', 'DELETE') NOT NULL,
    valor_antigo DECIMAL(10,2),
    forma_pagamento_antiga ENUM('Dinheiro', 'Cartão', 'Pix', 'Convênio'),
    status_pagamento_antigo ENUM('Pendente', 'Pago', 'Cancelado'),
    data_pagamento_antiga DATETIME,
    data_log DATETIME DEFAULT CURRENT_TIMESTAMP
);


DELIMITER //

CREATE TRIGGER trg_pagamento_update
BEFORE UPDATE ON pagamentos
FOR EACH ROW
BEGIN
    INSERT INTO log_pagamentos (
        id_pagamento,
        acao,
        valor_antigo,
        forma_pagamento_antiga,
        status_pagamento_antigo,
        data_pagamento_antiga
    ) VALUES (
        OLD.id,
        'UPDATE',
        OLD.valor,
        OLD.forma_pagamento,
        OLD.status_pagamento,
        OLD.data_pagamento
    );
END;
//

DELIMITER ;


DELIMITER //

CREATE TRIGGER trg_pagamento_delete
BEFORE DELETE ON pagamentos
FOR EACH ROW
BEGIN
    INSERT INTO log_pagamentos (
        id_pagamento,
        acao,
        valor_antigo,
        forma_pagamento_antiga,
        status_pagamento_antigo,
        data_pagamento_antiga
    ) VALUES (
        OLD.id,
        'DELETE',
        OLD.valor,
        OLD.forma_pagamento,
        OLD.status_pagamento,
        OLD.data_pagamento
    );
END;
//

DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_cadastrar_consulta(
    IN pid_paciente INT,
    IN pid_medico INT,
    IN pdata_consulta DATETIME,
    IN pobservacoes TEXT
)
BEGIN
    DECLARE conflito INT;

    SET conflito = (
        SELECT COUNT(*)
        FROM consultas
        WHERE id_medico = pid_medico
          AND data_consulta BETWEEN DATE_SUB(pdata_consulta, INTERVAL 29 MINUTE) 
                                AND DATE_ADD(pdata_consulta, INTERVAL 29 MINUTE)
    );

    IF conflito > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Conflito de agenda para este médico neste horário.';
    ELSE
        INSERT INTO consultas (id_paciente, id_medico, data_consulta, observacoes)
        VALUES (pid_paciente, pid_medico, pdata_consulta, pobservacoes);
    END IF;
END //
DELIMITER ;


DELIMITER //

DELIMITER //

CREATE PROCEDURE sp_relatorio_pagamentos(IN data_inicio DATE, IN data_fim DATE)
BEGIN
    SELECT 
        COUNT(DISTINCT c.id) AS total_consultas,
        IFNULL(SUM(CASE 
            WHEN p.status_pagamento = 'Pago' THEN p.valor 
            ELSE 0 
        END), 0) AS faturamento_total
    FROM consultas c
    LEFT JOIN pagamentos p ON c.id = p.id_consulta
    WHERE DATE(c.data_consulta) BETWEEN data_inicio AND data_fim;
END //

DELIMITER ;


CREATE OR REPLACE VIEW vw_consultas_por_data AS
SELECT
    c.id,
    c.data_consulta,
    p.nome AS nome_paciente,
    m.nome AS nome_medico,
    c.observacoes
FROM consultas c
JOIN pacientes p ON c.id_paciente = p.id
JOIN medicos m ON c.id_medico = m.id;















