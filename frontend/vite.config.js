//So basically after defining all the versions of all the front-end dependencies including vite in package.json,
//and after running the nmp install command which installs everything in package.json,
//the package-lock.json file is created and the node_modules folder along with all the things in it is created by running this command.
//this vite.config.js file is then defined manually.

//Import necessary modules from Vite:
import { defineConfig } from 'vite' //this imports the defineConfig function from Vite.
//It's used to define configuration objects in a type-safe way. This helps with better autocompletion and validation when using
//TypeScript (though it works in JavaScript as well).
import vue from '@vitejs/plugin-vue' //this imports the Vue plugin for Vite.
//It enables Vite to handle Vue files (.vue), compile Vue components, and optimize them for the build process.

//Path and URL handling for the project:
import path from 'path'; // Importing Node.js 'path' module to handle and resolve file paths.
import { fileURLToPath } from 'url'; //Importing the 'fileURLToPath' function from Node.sjs's 'url' module to work with ES modules and resolve file URLs to file paths.

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// '__dirname' is a variable used to reference the current directory. Since ES modules don't have '__dirname' by default, this line ensures the path os the current
//module's URL to a file path.

//This part is where you define the actual configuration for your Vite project:
// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  // base: Configures the base URL for the project, which can vary depending on whether we're in development or production mode.
  base:
      mode == "development"
          ? "http://localhost:5173/"
          : "/static/api/spa/", //In production mdoe, the base URL will be a relative path for deployment (e.g., '/static/api/spa/').
  // build: Configures build-specific options
  build: {
      emptyOutDir: true, // Ensures that the output directory is emptied before a new build. This avoids leftover files from previous builds.
      outDir: "../api/static/api/spa", //Specifies the output directory for the build project files. In this case, it will save to '../api/static/api/spa'.
  },
  //plugins: This section includes plugins to extend Vite's functionality.
  plugins: [vue()], //tells Vite to use the Vue plugin to handle '.vue' files (single-file components) during development and the build process.
  //resolve: this secion configures module resolution.
  resolve: {
      alias: {
          '@': path.resolve(__dirname, './src'), //Sets up an alias for importing files from the 'src' folder.
          //Intead of using relative paths like '../../src/components', you can use '@/components' to reference the 'src/components' folder.
      },
  },
}));

//export default means the configuration object is being exported as the default export from this file,
//so it can be used by Vite when it runs.

//definedConfig({...}) is a helper function provided by Vite to define the configuration.
//It makes it easier to use Vite's configuration in a type-safe way and provides better autocompletion support in editors (like VSCode).

//plugins: [vue()] tells Vite to use the Vue plugin (@vitejs/plugin-vue) for handling .vue files.
//vue() is a calling the Vue plugin's function to enable support for Vue 3.x single-file components.
//The plugin allows Vite to compile and bundle Vue components correctly during development and productions builds.
//This means that Vite will:
//Recognize .vue files in the project.
//Enable hot module replacement (HMR) for Vue components during development.
//Optimize Vue components when building the project for production.

//path and fileURLToPath are Node.js utilities that help resolve and manage file paths, particularly when dealing with module-based syste,s (ES modules).

//Since ES modules don't have __dirname, it is defined manyally using path.dirname(fileURLToPath(import.meta.url)) to resilve the directory of the current file.

//base: configuration: depending on whether you're in development or production mode, the base path for the project is set. For development, it points to the
//local server URL (http://localhost:5173/), and for production, it uses a relative path (/static/api/spa/).

//build: configuration: Ensures that the build output directory is emprtied before a new build (emptyOutDir: true).
//Specifies the output directory as ../api/static/api/spa.

//plugins: configuration: Uses the Vye plugin (vue()) to enable Vue-specific handling in Vite, such as compiling .vue files and enabling Hot Module Replacement (HMR) in development.

//resolve: configuration: Sets up an alias for the src directory, so instead of using long relative paths for imports (e.g., ../../src/components), you can simply user @/components
//to reference the src/components folder.