import { render, screen } from '@testing-library/react';
import App from './App';

test('Comprueba que la interfaz cargue y muestre el titulo del sistema', () => {
  render(<App />);
  
  // Buscamos alguna palabra clave que sepamos que esta en su interfaz visual.
  // "Biblioteca" es casi segura, pero si falla, puedes cambiarla por "Socios" o "Libros"
  const textoEnPantalla = screen.getByText(/Biblioteca/i);
  
  expect(textoEnPantalla).toBeInTheDocument();
});