export interface Input {
    id: number;
    category_id: number;
    name: string;
    brand?: string;
    description?: string;
    unit_of_measure: string;
    unit_price: number;
    minimum_stock: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
  }
  
  export interface InputCreate {
    category_id: number;
    name: string;
    brand?: string;
    description?: string;
    unit_of_measure: string;
    unit_price: number;
    minimum_stock: number;
    is_active: boolean;
  }
  
  export interface InputUpdate {
    category_id?: number;
    name?: string;
    brand?: string;
    description?: string;
    unit_of_measure?: string;
    unit_price?: number;
    minimum_stock?: number;
    is_active?: boolean;
  }