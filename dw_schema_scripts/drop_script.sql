IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[customer_interactions]') AND type in (N'U'))
DROP TABLE [dbo].[customer_interactions]
GO;

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[marketing_campaigns]') AND type in (N'U'))
DROP TABLE [dbo].[marketing_campaigns]
GO;

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[product_inventory]') AND type in (N'U'))
DROP TABLE [dbo].[product_inventory]
GO;

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sales_data]') AND type in (N'U'))
DROP TABLE [dbo].[sales_data]
GO;

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[regional_sales_targets]') AND type in (N'U'))
DROP TABLE [dbo].[regional_sales_targets]
GO;

delete 
  FROM [dbo].[DataProcessingMetadata]