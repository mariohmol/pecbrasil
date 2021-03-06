
drop TABLE `despesatipo` ;
-- --------------------------------------------------------

--
-- Estrutura da tabela `despesatipo`
--

CREATE TABLE `despesatipo` (
  `id_despesatipo` int(11) NOT NULL AUTO_INCREMENT,
  `nome_despesatipo` varchar(150) DEFAULT NULL,
  `cor_despesatipo` varchar(10) DEFAULT NULL,
  `desc_despesatipo` text,
  PRIMARY KEY (`id_despesatipo`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Extraindo dados da tabela `despesatipo`
--

INSERT INTO `despesatipo` (`id_despesatipo`, `nome_despesatipo`, `cor_despesatipo`, `desc_despesatipo`) VALUES
(1, 'ASSINATURA DE PUBLICACOES', '#f1c40f', NULL),
(2, 'COMBUSTÖVEIS E LUBRIFICANTES.', '#3498db', NULL),
(3, 'CONSULTORIAS, PESQUISAS E TRABALHOS TCNICOS.', '#b4b735', NULL),
(4, 'DIVULGACAO DA ATIVIDADE PARLAMENTAR', '#eb696d', NULL),
(5, 'COMBUSTIVEIS E LUBRIFICANTES', '#3498db', NULL),
(6, 'CONSULTORIAS', '#b4b735', NULL),
(7, 'EMISSAO BILHETE AEREO', '#df1e25', NULL),
(8, 'FORNECIMENTO DE ALIMENTACAO DO PARLAMENTAR', '#086aab', NULL),
(9, 'HOSPEDAGEM ,EXCETO DO PARLAMENTAR NO DISTRITO FEDERAL.', '#be5629', NULL),
(10, 'LOCACAO DE VEICULOS AUTOMOTORES OU FRETAMENTO', '#de0505', NULL),
(11, 'MANUTENCAO DE ESCRITORIO DE APOIO A ATIVIDADE', '#f06b6c', NULL),
(12, 'PASSAGENS AEREAS E FRETAMENTO DE AERONAVES', '#636aa9', NULL),
(13, 'SERVICO DE SEGURANCA PRESTADO POR EMPRESA ESPECIALIZADA', '#2c3d50', NULL),
(14, 'SERVICOS POSTAIS', '#a2cd39', NULL),
(15, 'TELEFONIA', '#e74b3b', NULL);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
