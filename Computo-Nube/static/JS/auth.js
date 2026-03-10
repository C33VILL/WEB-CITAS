// Gestión de Estado de Autenticación
const Auth = {
    // Simular el inicio de sesión
    login(username, password) {
        if (username === 'admin' && password === 'admin123') {
            const userData = {
                user: username,
                token: 'fake-jwt-token-' + Math.random().toString(36).substr(2),
                loginTime: new Date().getTime()
            };
            // Guardamos el estado en el cliente
            localStorage.setItem('vet_auth', JSON.stringify(userData));
            return true;
        }
        return false;
    },

    // Verificar si el usuario está autenticado
    isAuthenticated() {
        const session = localStorage.getItem('vet_auth');
        if (!session) return false;

        const data = JSON.parse(session);
        // Expiración simple (ej. 1 hora)
        const now = new Date().getTime();
        if (now - data.loginTime > 3600000) {
            this.logout();
            return false;
        }
        return true;
    },

    // Cerrar sesión
    logout() {
        localStorage.removeItem('vet_auth');
        window.location.href = '/login';
    }
};
