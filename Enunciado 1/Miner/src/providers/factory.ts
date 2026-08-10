import { IMiningProvider } from '@/core/interfaces/provider';
import { ProviderType } from '@/core/interfaces/spec';

export class ProviderFactory {
  private static providers: Map<ProviderType, IMiningProvider> = new Map();

  public static register(type: ProviderType, provider: IMiningProvider): void {
    this.providers.set(type, provider);
  }

  public static getProvider(type: ProviderType): IMiningProvider {
    const provider = this.providers.get(type);
    if (!provider) {
      throw new Error(`Provider [${type}] não foi registrado no sistema.`);
    }
    return provider;
  }
}