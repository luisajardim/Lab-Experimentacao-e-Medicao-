import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename } : { filename: string }) => filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			}
		})
	],
	server: {
		fs: {
			allow: ['..']
		}
	},
	ssr: {
		noExternal: ['lucide-svelte']
	}
});
