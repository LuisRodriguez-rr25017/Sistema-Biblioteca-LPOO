import { render, screen } from '@testing-library/react';
import App from './App';

test('Comprueba que la interfaz cargue y muestre el titulo del sistema', () => {
  render(<App />);

         
  const textoEnPantalla = screen.getByText(/Biblioteca/i);
  
  expect(textoEnPantalla).toBeInTheDocument();
});
