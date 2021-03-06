USE [swimcoachdb]
GO
/****** Object:  Table [dbo].[athlete]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[athlete](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[firstname] [nvarchar](100) NOT NULL,
	[lastname] [nvarchar](100) NOT NULL,
	[dateofbirth] [date] NULL,
	[club] [uniqueidentifier] NULL,
 CONSTRAINT [PK_athlete] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[club]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[club](
	[idclub] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](80) NOT NULL,
	[postaladdress] [nvarchar](100) NOT NULL,
	[postalzipcode] [nvarchar](13) NOT NULL,
	[postalcity] [nvarchar](50) NOT NULL,
	[visitingaddress] [nvarchar](100) NOT NULL,
	[visitingzipcode] [nvarchar](13) NOT NULL,
	[visitingcity] [nvarchar](50) NOT NULL,
	[registrationno] [nvarchar](10) NOT NULL,
	[rowkey] [uniqueidentifier] NOT NULL CONSTRAINT [DF_club_rowkey]  DEFAULT (newid()),
	[description] [nvarchar](500) NOT NULL CONSTRAINT [DF_club_description]  DEFAULT (''),
	[profilepicture] [int] NULL,
 CONSTRAINT [PK_club] PRIMARY KEY CLUSTERED 
(
	[idclub] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[group]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[group](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NULL,
	[description] [nvarchar](512) NULL,
	[owner] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[groupmember]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[groupmember](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[athlete] [int] NULL,
	[group] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[profile]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[profile](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[user] [int] NULL,
	[firstname] [nvarchar](100) NOT NULL,
	[lastname] [nvarchar](100) NOT NULL,
	[email] [nvarchar](200) NOT NULL,
	[clubkey] [uniqueidentifier] NULL,
 CONSTRAINT [PK_Table1] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[session]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[session](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[iduser] [int] NOT NULL,
	[logintime] [datetime] NOT NULL,
	[logouttime] [datetime] NULL,
	[active] [int] NOT NULL,
	[sessiontoken] [nvarchar](40) NOT NULL,
	[workstation] [nvarchar](20) NOT NULL CONSTRAINT [DF_session_workstation]  DEFAULT (''),
 CONSTRAINT [PK_Table_2] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[trainingresult]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[trainingresult](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[resulttype] [int] NOT NULL,
	[trainingsession] [int] NULL,
	[timeresult_ms] [int] NULL,
	[athlete] [int] NOT NULL,
	[owner] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[trainingsession]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[trainingsession](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](100) NOT NULL,
	[description] [nvarchar](250) NOT NULL,
	[fromtime] [datetime] NULL,
	[totime] [datetime] NULL,
	[group] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[user]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[user](
	[iduser] [int] IDENTITY(1,1) NOT NULL,
	[email] [nvarchar](200) NOT NULL,
	[hash] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_Table_1] PRIMARY KEY CLUSTERED 
(
	[iduser] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[userfile]    Script Date: 2016-09-07 21:33:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[userfile](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[filetype] [nvarchar](40) NOT NULL,
	[owner] [nvarchar](40) NOT NULL,
	[filename] [nvarchar](128) NULL DEFAULT (N''),
 CONSTRAINT [PK_userfile] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
ALTER TABLE [dbo].[athlete]  WITH CHECK ADD  CONSTRAINT [FK_athlete_athlete] FOREIGN KEY([id])
REFERENCES [dbo].[athlete] ([id])
GO
ALTER TABLE [dbo].[athlete] CHECK CONSTRAINT [FK_athlete_athlete]
GO
ALTER TABLE [dbo].[club]  WITH CHECK ADD  CONSTRAINT [FK_club_profilepicture] FOREIGN KEY([profilepicture])
REFERENCES [dbo].[userfile] ([id])
GO
ALTER TABLE [dbo].[club] CHECK CONSTRAINT [FK_club_profilepicture]
GO
ALTER TABLE [dbo].[group]  WITH CHECK ADD FOREIGN KEY([owner])
REFERENCES [dbo].[club] ([idclub])
GO
ALTER TABLE [dbo].[groupmember]  WITH CHECK ADD FOREIGN KEY([athlete])
REFERENCES [dbo].[athlete] ([id])
GO
ALTER TABLE [dbo].[groupmember]  WITH CHECK ADD FOREIGN KEY([group])
REFERENCES [dbo].[group] ([id])
GO
ALTER TABLE [dbo].[trainingsession]  WITH CHECK ADD FOREIGN KEY([group])
REFERENCES [dbo].[group] ([id])
GO
