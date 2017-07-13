use mydb;

DROP VIEW IF EXISTS vw_insumo_by_imoveis;
CREATE VIEW vw_insumo_by_imoveis 
AS   
  SELECT   i.idinsumo AS insumo
		 , i.descricao AS descricao
         , ci.imoveis AS imovel
         
  FROM  insumo i, compra_insumo ci
  WHERE ci.insumo = i.idinsumo