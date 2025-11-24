USE [ERP_DB]
GO
/****** Object:  Table [dbo].[DocumentosFiscais]    Script Date: 24-11-2025 22:06:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DocumentosFiscais](
	[DocumentoId] [int] IDENTITY(1,1) NOT NULL,
	[TipoDocumento] [nvarchar](20) NULL,
	[ChaveAcesso] [nvarchar](50) NULL,
	[NumeroDocumento] [nvarchar](30) NULL,
	[Serie] [nvarchar](10) NULL,
	[DataEmissao] [datetime] NULL,
	[NaturezaOperacao] [nvarchar](150) NULL,
	[EntidadeEmitenteId] [int] NULL,
	[EntidadeDestinatarioId] [int] NULL,
	[ValorTotal] [decimal](18, 2) NULL,
	[ImpostosTotais] [decimal](18, 2) NULL,
	[Estado] [nvarchar](20) NULL,
	[CaminhoXML] [nvarchar](500) NULL,
	[DataImportacao] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[DocumentoId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Entidades]    Script Date: 24-11-2025 22:06:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Entidades](
	[EntidadeId] [int] IDENTITY(1,1) NOT NULL,
	[Nome] [nvarchar](200) NOT NULL,
	[NUIT] [nvarchar](30) NULL,
	[Tipo] [nvarchar](50) NULL,
	[Email] [nvarchar](150) NULL,
	[Telefone] [nvarchar](50) NULL,
	[Endereco] [nvarchar](255) NULL,
	[DataRegisto] [datetime] NULL,
	[DataAtualizacao] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[EntidadeId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ImpostosDocumento]    Script Date: 24-11-2025 22:06:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ImpostosDocumento](
	[ImpostoId] [int] IDENTITY(1,1) NOT NULL,
	[DocumentoId] [int] NULL,
	[TipoImposto] [nvarchar](50) NULL,
	[BaseCalculo] [decimal](18, 2) NULL,
	[ValorImposto] [decimal](18, 2) NULL,
	[Aliquota] [decimal](5, 2) NULL,
PRIMARY KEY CLUSTERED 
(
	[ImpostoId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ItensDocumento]    Script Date: 24-11-2025 22:06:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ItensDocumento](
	[ItemId] [int] IDENTITY(1,1) NOT NULL,
	[DocumentoId] [int] NULL,
	[CodigoProduto] [nvarchar](100) NULL,
	[Descricao] [nvarchar](255) NULL,
	[Quantidade] [decimal](18, 3) NULL,
	[ValorUnitario] [decimal](18, 4) NULL,
	[ValorTotal] [decimal](18, 2) NULL,
	[NCM] [nvarchar](20) NULL,
	[CFOP] [nvarchar](10) NULL,
	[CST] [nvarchar](10) NULL,
	[AliquotaIVA] [decimal](5, 2) NULL,
	[DataRegisto] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ItemId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[LogsImportacao]    Script Date: 24-11-2025 22:06:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LogsImportacao](
	[LogId] [int] IDENTITY(1,1) NOT NULL,
	[ChaveAcesso] [nvarchar](50) NULL,
	[Estado] [nvarchar](30) NULL,
	[Mensagem] [nvarchar](max) NULL,
	[DataLog] [datetime] NULL,
	[XMLFile] [nvarchar](255) NULL,
	[IPOrigem] [nvarchar](45) NULL,
PRIMARY KEY CLUSTERED 
(
	[LogId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SchemaVersions]    Script Date: 24-11-2025 22:06:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SchemaVersions](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[ScriptName] [nvarchar](255) NOT NULL,
	[Applied] [datetime] NOT NULL,
 CONSTRAINT [PK_SchemaVersions_Id] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[DocumentosFiscais] ON 
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (1, N'NFe', N'33250112345678000123550010000000011999999999', N'1001', N'1', CAST(N'2025-11-03T19:15:30.000' AS DateTime), N'Venda de produtos diversos', 1, 2, CAST(155000.00 AS Decimal(18, 2)), CAST(15500.00 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-03T07:31:53.300' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (2, N'NFe', N'33250198765432000145550010000000021987654321', N'2', N'1', CAST(N'2025-01-20T19:15:30.000' AS DateTime), N'Venda de mercadorias', 3, 4, CAST(1000.00 AS Decimal(18, 2)), CAST(150.00 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-03T07:43:21.080' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (3, N'NFe', N'{chave}', N'{nNF}', N'1', NULL, N'Venda de mercadorias', 5, 6, NULL, NULL, N'Recebido', NULL, CAST(N'2025-11-03T07:46:04.840' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (4, N'NFe', N'35250198765432000123550010000000029876543210', N'2', N'1', CAST(N'2025-01-15T14:15:00.000' AS DateTime), N'Venda de peças automotivas', 7, 8, CAST(300.00 AS Decimal(18, 2)), CAST(48.00 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-03T07:46:39.820' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (5, N'NFe', N'35250199887766000123550010000000039988776600', N'3', N'1', CAST(N'2025-02-04T00:10:00.000' AS DateTime), N'Venda de lanches', 9, 10, CAST(50.00 AS Decimal(18, 2)), CAST(7.50 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-03T07:47:03.227' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (6, N'NFe', N'35250188776655000123550010000000048877665500', N'4', N'1', CAST(N'2025-02-05T12:20:00.000' AS DateTime), N'Venda de produtos de panificação', 11, 12, CAST(300.00 AS Decimal(18, 2)), CAST(45.00 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-03T07:47:14.297' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (7, N'NFe', N'35250155667788000123550010000000055566778800', N'5', N'1', CAST(N'2025-03-12T16:30:00.000' AS DateTime), N'Venda de medicamentos', 13, 14, CAST(120.00 AS Decimal(18, 2)), CAST(18.00 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-03T07:47:23.943' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (8, N'NFe', N'35250112345678000123550010000000011234567891', N'1', N'1', CAST(N'2025-01-10T19:35:00.000' AS DateTime), N'Venda de alimentos', 1, 15, CAST(100.00 AS Decimal(18, 2)), CAST(15.00 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-03T07:49:05.510' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (9, N'NFe', N'35250122113344000123550010000000092211334400', N'9', N'1', CAST(N'2025-06-03T18:30:00.000' AS DateTime), N'Venda de eletrônicos', 16, 17, CAST(4500.00 AS Decimal(18, 2)), CAST(675.00 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-03T09:38:06.520' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (12, N'NFe', N'35251112345678000123550010000000011234567894', N'1', N'1', CAST(N'2025-11-24T18:07:00.000' AS DateTime), N'VENDA DE MERCADORIA', 1, 19, CAST(105.00 AS Decimal(18, 2)), CAST(26.65 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-24T18:53:00.977' AS DateTime))
GO
INSERT [dbo].[DocumentosFiscais] ([DocumentoId], [TipoDocumento], [ChaveAcesso], [NumeroDocumento], [Serie], [DataEmissao], [NaturezaOperacao], [EntidadeEmitenteId], [EntidadeDestinatarioId], [ValorTotal], [ImpostosTotais], [Estado], [CaminhoXML], [DataImportacao]) VALUES (13, N'NFe', N'35251112345678000123550010000000041234567894', N'4', N'1', CAST(N'2025-11-24T19:30:00.000' AS DateTime), N'VENDA DE MERCADORIA COM FRETE', 1, 19, CAST(115.00 AS Decimal(18, 2)), CAST(26.65 AS Decimal(18, 2)), N'Recebido', NULL, CAST(N'2025-11-24T19:26:45.077' AS DateTime))
GO
SET IDENTITY_INSERT [dbo].[DocumentosFiscais] OFF
GO
SET IDENTITY_INSERT [dbo].[Entidades] ON 
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (1, N'EMPRESA EXEMPLO LTDA', N'12345678000123', N'Empresa', NULL, NULL, NULL, CAST(N'2025-11-03T07:31:53.220' AS DateTime), CAST(N'2025-11-24T19:26:45.070' AS DateTime))
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (2, N'Cliente Teste SA', N'98765432000198', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T07:31:53.250' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (3, N'Empresa Exemplo Lda', N'12345678000145', N'Empresa', NULL, NULL, NULL, CAST(N'2025-11-03T07:43:21.030' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (4, N'Cliente Teste SA', N'98765432000145', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T07:43:21.037' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (5, N'{emitNome}', N'{emitCNPJ}', N'Empresa', NULL, NULL, NULL, CAST(N'2025-11-03T07:46:04.833' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (6, N'{destNome}', N'{destCNPJ}', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T07:46:04.833' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (7, N'Auto Peças São Jorge LTDA', N'98765432000123', N'Empresa', NULL, NULL, NULL, CAST(N'2025-11-03T07:46:39.813' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (8, N'Oficina do João', N'15487965000102', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T07:46:39.813' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (9, N'Lanchonete Sabor Paulista', N'99887766000123', N'Empresa', NULL, NULL, NULL, CAST(N'2025-11-03T07:47:03.220' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (10, N'Cliente Ana Maria', N'12312312000177', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T07:47:03.223' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (11, N'Padaria Pão Quente LTDA', N'88776655000123', N'Empresa', NULL, NULL, NULL, CAST(N'2025-11-03T07:47:14.250' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (12, N'Restaurante Central', N'11447788000166', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T07:47:14.297' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (13, N'Drogaria Vida e Saúde LTDA', N'55667788000123', N'Empresa', NULL, NULL, NULL, CAST(N'2025-11-03T07:47:23.943' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (14, N'Cliente Pedro Alves', N'44223311000155', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T07:47:23.943' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (15, N'Cliente José da Silva', N'45896532000178', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T07:49:05.503' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (16, N'TecnoBrasil Informática LTDA', N'22113344000123', N'Empresa', NULL, NULL, NULL, CAST(N'2025-11-03T09:38:06.407' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (17, N'Cliente Lucas Andrade', N'99887711000177', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-03T09:38:06.423' AS DateTime), NULL)
GO
INSERT [dbo].[Entidades] ([EntidadeId], [Nome], [NUIT], [Tipo], [Email], [Telefone], [Endereco], [DataRegisto], [DataAtualizacao]) VALUES (19, N'NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL', N'88888888000188', N'Cliente', NULL, NULL, NULL, CAST(N'2025-11-24T18:53:00.947' AS DateTime), CAST(N'2025-11-24T19:26:45.073' AS DateTime))
GO
SET IDENTITY_INSERT [dbo].[Entidades] OFF
GO
SET IDENTITY_INSERT [dbo].[ItensDocumento] ON 
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (1, 1, N'P001', N'Notebook Dell Inspiron 15', CAST(2.000 AS Decimal(18, 3)), CAST(55000.0000 AS Decimal(18, 4)), CAST(110000.00 AS Decimal(18, 2)), N'84713012', N'5102', NULL, NULL, CAST(N'2025-11-03T07:31:53.340' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (2, 1, N'P002', N'Monitor Samsung 24"', CAST(3.000 AS Decimal(18, 3)), CAST(15000.0000 AS Decimal(18, 4)), CAST(45000.00 AS Decimal(18, 2)), N'85285200', N'5102', NULL, NULL, CAST(N'2025-11-03T07:31:53.357' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (3, 2, N'001', N'Produto Teste', CAST(10.000 AS Decimal(18, 3)), CAST(100.0000 AS Decimal(18, 4)), CAST(1000.00 AS Decimal(18, 2)), N'22030000', N'5101', NULL, NULL, CAST(N'2025-11-03T07:43:21.123' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (4, 3, N'{codigo}', N'{descricao}', NULL, NULL, NULL, N'{ncm}', N'{cfop}', NULL, NULL, CAST(N'2025-11-03T07:46:04.843' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (5, 4, N'032', N'Filtro de Óleo', CAST(10.000 AS Decimal(18, 3)), CAST(30.0000 AS Decimal(18, 4)), CAST(300.00 AS Decimal(18, 2)), N'84212300', N'5102', NULL, NULL, CAST(N'2025-11-03T07:46:39.823' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (6, 5, N'101', N'X-Salada Completo', CAST(2.000 AS Decimal(18, 3)), CAST(25.0000 AS Decimal(18, 4)), CAST(50.00 AS Decimal(18, 2)), N'16010000', N'5102', NULL, NULL, CAST(N'2025-11-03T07:47:03.233' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (7, 6, N'210', N'Pão Francês 1kg', CAST(20.000 AS Decimal(18, 3)), CAST(15.0000 AS Decimal(18, 4)), CAST(300.00 AS Decimal(18, 2)), N'19052010', N'5102', NULL, NULL, CAST(N'2025-11-03T07:47:14.297' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (8, 7, N'600', N'Paracetamol 750mg', CAST(15.000 AS Decimal(18, 3)), CAST(8.0000 AS Decimal(18, 4)), CAST(120.00 AS Decimal(18, 2)), N'30045090', N'5102', NULL, NULL, CAST(N'2025-11-03T07:47:23.950' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (9, 8, N'001', N'Arroz Tipo 1 5kg', CAST(5.000 AS Decimal(18, 3)), CAST(20.0000 AS Decimal(18, 4)), CAST(100.00 AS Decimal(18, 2)), N'10063011', N'5102', NULL, NULL, CAST(N'2025-11-03T07:49:05.513' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (13, 12, N'0001', N'PRODUTO DE TESTE NFE 4.00', CAST(1.000 AS Decimal(18, 3)), CAST(100.0000 AS Decimal(18, 4)), CAST(100.00 AS Decimal(18, 2)), N'96081000', N'5102', NULL, NULL, CAST(N'2025-11-24T18:53:00.993' AS DateTime))
GO
INSERT [dbo].[ItensDocumento] ([ItemId], [DocumentoId], [CodigoProduto], [Descricao], [Quantidade], [ValorUnitario], [ValorTotal], [NCM], [CFOP], [CST], [AliquotaIVA], [DataRegisto]) VALUES (14, 13, N'0004', N'PRODUTO COM FRETE', CAST(1.000 AS Decimal(18, 3)), CAST(100.0000 AS Decimal(18, 4)), CAST(100.00 AS Decimal(18, 2)), N'96081000', N'5102', NULL, NULL, CAST(N'2025-11-24T19:26:45.080' AS DateTime))
GO
SET IDENTITY_INSERT [dbo].[ItensDocumento] OFF
GO
SET IDENTITY_INSERT [dbo].[SchemaVersions] ON 
GO
INSERT [dbo].[SchemaVersions] ([Id], [ScriptName], [Applied]) VALUES (1, N'ERP.Api.Infrastructure.Migrations.001_create_core.sql', CAST(N'2025-11-03T07:16:17.080' AS DateTime))
GO
INSERT [dbo].[SchemaVersions] ([Id], [ScriptName], [Applied]) VALUES (2, N'ERP.Api.Infrastructure.Migrations.002_alter_core_add_DataAtualizacao.sql', CAST(N'2025-11-03T10:15:32.387' AS DateTime))
GO
SET IDENTITY_INSERT [dbo].[SchemaVersions] OFF
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__Document__B1545512A4B626BF]    Script Date: 24-11-2025 22:06:41 ******/
ALTER TABLE [dbo].[DocumentosFiscais] ADD UNIQUE NONCLUSTERED 
(
	[ChaveAcesso] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[DocumentosFiscais] ADD  DEFAULT ('Recebido') FOR [Estado]
GO
ALTER TABLE [dbo].[DocumentosFiscais] ADD  DEFAULT (getdate()) FOR [DataImportacao]
GO
ALTER TABLE [dbo].[Entidades] ADD  DEFAULT (getdate()) FOR [DataRegisto]
GO
ALTER TABLE [dbo].[ItensDocumento] ADD  DEFAULT (getdate()) FOR [DataRegisto]
GO
ALTER TABLE [dbo].[LogsImportacao] ADD  DEFAULT (getdate()) FOR [DataLog]
GO
ALTER TABLE [dbo].[DocumentosFiscais]  WITH CHECK ADD FOREIGN KEY([EntidadeEmitenteId])
REFERENCES [dbo].[Entidades] ([EntidadeId])
GO
ALTER TABLE [dbo].[DocumentosFiscais]  WITH CHECK ADD FOREIGN KEY([EntidadeDestinatarioId])
REFERENCES [dbo].[Entidades] ([EntidadeId])
GO
ALTER TABLE [dbo].[ImpostosDocumento]  WITH CHECK ADD FOREIGN KEY([DocumentoId])
REFERENCES [dbo].[DocumentosFiscais] ([DocumentoId])
GO
ALTER TABLE [dbo].[ItensDocumento]  WITH CHECK ADD FOREIGN KEY([DocumentoId])
REFERENCES [dbo].[DocumentosFiscais] ([DocumentoId])
GO
ALTER TABLE [dbo].[DocumentosFiscais]  WITH CHECK ADD CHECK  (([TipoDocumento]='Outro' OR [TipoDocumento]='Recibo' OR [TipoDocumento]='NFSe' OR [TipoDocumento]='NFe'))
GO
ALTER TABLE [dbo].[Entidades]  WITH CHECK ADD CHECK  (([Tipo]='Empresa' OR [Tipo]='Cliente' OR [Tipo]='Fornecedor'))
GO
